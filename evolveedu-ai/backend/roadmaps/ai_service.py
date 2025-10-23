# roadmaps/ai_service.py
import requests
import json
import time
import re
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Skill, SkillCategory, CareerPath, PersonalizedRoadmap,
    RoadmapMilestone, SkillAssessment, LearningResource
)


class RoadmapAIService:

    @staticmethod
    def call_huggingface_api(prompt, max_retries=3, delay=1):
        """Make API call to Hugging Face with retry logic"""
        headers = {
            "Authorization": f"Bearer {getattr(settings, 'HUGGINGFACE_API_KEY', '')}",
            "Content-Type": "application/json"
        }

        # Using Flan-T5 for better instruction following
        api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(api_url, headers=headers, json=payload)

                if response.status_code == 503:
                    time.sleep(delay * (attempt + 1))
                    continue
                elif response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get('generated_text', '')
                    return result.get('generated_text', '')
                else:
                    print(f"HuggingFace API error: {response.status_code} - {response.text}")
                    break

            except Exception as e:
                print(f"API call attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(delay)

        return None

    @staticmethod
    def generate_personalized_roadmap(user, career_goal, current_skills, experience_level,
                                      time_commitment, target_months, learning_style, focus_areas):
        """Generate a personalized learning roadmap using AI"""
        try:
            current_skills_str = ", ".join(current_skills) if current_skills else "None specified"
            focus_areas_str = ", ".join(focus_areas) if focus_areas else "General development"

            prompt = f"""Create a learning roadmap for: {career_goal}

Current Skills: {current_skills_str}
Experience: {experience_level}
Time: {time_commitment} hours/week
Timeline: {target_months} months
Learning Style: {learning_style}
Focus: {focus_areas_str}

Provide a structured plan with:
1. Roadmap title and description
2. 4-6 key milestones with skills to learn
3. Estimated hours for each milestone
4. Weekly goals for first 4 weeks
5. Learning recommendations

Format as clear sections with specific, actionable steps."""

            ai_response = RoadmapAIService.call_huggingface_api(prompt)

            if ai_response:
                roadmap = RoadmapAIService._parse_roadmap_response(
                    ai_response, user, career_goal, target_months, time_commitment
                )
                return roadmap
            else:
                raise Exception("Failed to get response from Hugging Face API")

        except Exception as e:
            print(f"Roadmap generation failed: {str(e)}")
            return RoadmapAIService._create_fallback_roadmap(
                user, career_goal, target_months, time_commitment
            )

    @staticmethod
    def _parse_roadmap_response(ai_response, user, career_goal, target_months, time_commitment):
        """Parse AI response and create roadmap in database"""
        try:
            # Extract roadmap title and description
            lines = ai_response.split('\n')
            title = f"Learning Path: {career_goal}"
            description = f"A personalized learning roadmap for {career_goal}"

            # Look for title in response
            for line in lines:
                if ('roadmap' in line.lower() or 'title' in line.lower()) and len(line) > 10:
                    title = line.strip().replace('Title:', '').replace('Roadmap:', '').strip()
                    break

            # Create roadmap
            roadmap = PersonalizedRoadmap.objects.create(
                user=user,
                title=title,
                description=description,
                start_date=timezone.now().date(),
                target_completion_date=timezone.now().date() + timedelta(days=target_months * 30),
                estimated_hours_per_week=time_commitment,
                status='active'
            )

            # Parse milestones from response
            milestones = RoadmapAIService._extract_milestones_from_response(ai_response, roadmap)

            # Parse weekly goals
            weekly_goals = RoadmapAIService._extract_weekly_goals_from_response(ai_response)
            roadmap.weekly_goals = weekly_goals

            # Parse recommendations
            recommendations = RoadmapAIService._extract_recommendations_from_response(ai_response)
            roadmap.personalized_recommendations = recommendations

            roadmap.save()

            return roadmap

        except Exception as e:
            print(f"Parsing error: {str(e)}")
            return RoadmapAIService._create_fallback_roadmap(
                user, career_goal, target_months, time_commitment
            )

    @staticmethod
    def _extract_milestones_from_response(ai_response, roadmap):
        """Extract milestones from AI response"""
        milestones = []
        lines = ai_response.split('\n')

        milestone_keywords = ['milestone', 'phase', 'step', 'stage', 'week', 'month']
        skill_keywords = ['learn', 'master', 'understand', 'practice', 'develop']

        current_milestone = None
        milestone_order = 1

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this line describes a milestone
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in milestone_keywords):
                if current_milestone:
                    milestones.append(current_milestone)

                # Extract milestone title
                title = line.replace(':', '').strip()
                if len(title) > 50:
                    title = title[:47] + "..."

                current_milestone = {
                    'title': title,
                    'description': '',
                    'skill_name': '',
                    'estimated_hours': 20,
                    'order': milestone_order
                }
                milestone_order += 1

            elif current_milestone and any(keyword in line_lower for keyword in skill_keywords):
                # This line describes what to learn
                if not current_milestone['description']:
                    current_milestone['description'] = line
                if not current_milestone['skill_name']:
                    current_milestone['skill_name'] = RoadmapAIService._extract_skill_name(line)

        # Add the last milestone
        if current_milestone:
            milestones.append(current_milestone)

        # Create milestone objects
        general_category = SkillCategory.objects.first() or SkillCategory.objects.create(name='General')

        for milestone_data in milestones:
            skill_name = milestone_data['skill_name'] or milestone_data['title']

            skill, created = Skill.objects.get_or_create(
                name=skill_name[:50],  # Limit length
                defaults={
                    'description': milestone_data['description'][:200],
                    'category': general_category,
                    'estimated_hours': milestone_data['estimated_hours']
                }
            )

            RoadmapMilestone.objects.create(
                roadmap=roadmap,
                title=milestone_data['title'],
                description=milestone_data['description'],
                skill=skill,
                estimated_hours=milestone_data['estimated_hours'],
                order=milestone_data['order']
            )

        return len(milestones)

    @staticmethod
    def _extract_skill_name(line):
        """Extract skill name from a line of text"""
        # Simple extraction - look for key terms
        words = line.split()
        skill_indicators = ['programming', 'development', 'analysis', 'design', 'management',
                            'communication', 'leadership', 'technical', 'software', 'data']

        for word in words:
            if word.lower() in skill_indicators:
                return word.capitalize()

        # Fallback: return first meaningful word
        for word in words:
            if len(word) > 3 and word.isalpha():
                return word.capitalize()

        return "General Skill"

    @staticmethod
    def _extract_weekly_goals_from_response(ai_response):
        """Extract weekly goals from AI response"""
        weekly_goals = []
        lines = ai_response.split('\n')

        current_week = 0
        for line in lines:
            line_lower = line.lower()
            if 'week' in line_lower and any(char.isdigit() for char in line):
                current_week += 1
                # Extract goal from line
                goal = line.strip()
                if ':' in goal:
                    goal = goal.split(':', 1)[1].strip()

                weekly_goals.append({
                    'week': current_week,
                    'goal': goal,
                    'focus_skills': [f'Week {current_week} skills']
                })

                if current_week >= 4:  # Limit to first 4 weeks
                    break

        return weekly_goals

    @staticmethod
    def _extract_recommendations_from_response(ai_response):
        """Extract recommendations from AI response"""
        recommendations = []
        lines = ai_response.split('\n')

        recommendation_keywords = ['recommend', 'suggest', 'tip', 'advice', 'consider']

        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in recommendation_keywords):
                cleaned_line = line.strip()
                if len(cleaned_line) > 10:
                    recommendations.append(cleaned_line)

                if len(recommendations) >= 5:  # Limit recommendations
                    break

        return recommendations

    @staticmethod
    def _create_fallback_roadmap(user, career_goal, target_months, time_commitment):
        """Create a basic fallback roadmap when AI fails"""
        roadmap = PersonalizedRoadmap.objects.create(
            user=user,
            title=f"Learning Path: {career_goal}",
            description=f"A structured learning path to achieve {career_goal}",
            start_date=timezone.now().date(),
            target_completion_date=timezone.now().date() + timedelta(days=target_months * 30),
            estimated_hours_per_week=time_commitment,
            status='active'
        )

        # Create basic milestones
        basic_milestones = [
            {
                'title': 'Foundation Skills',
                'description': 'Build fundamental knowledge and skills',
                'hours': int(target_months * time_commitment * 0.3)
            },
            {
                'title': 'Intermediate Development',
                'description': 'Develop intermediate level competencies',
                'hours': int(target_months * time_commitment * 0.4)
            },
            {
                'title': 'Advanced Practice',
                'description': 'Advanced skills and real-world application',
                'hours': int(target_months * time_commitment * 0.3)
            }
        ]

        general_category = SkillCategory.objects.first() or SkillCategory.objects.create(name='General')

        for i, milestone in enumerate(basic_milestones):
            skill, created = Skill.objects.get_or_create(
                name=f"{career_goal} - {milestone['title']}"[:50],
                defaults={
                    'description': milestone['description'],
                    'category': general_category,
                    'estimated_hours': milestone['hours']
                }
            )

            RoadmapMilestone.objects.create(
                roadmap=roadmap,
                title=milestone['title'],
                description=milestone['description'],
                skill=skill,
                estimated_hours=milestone['hours'],
                order=i + 1
            )

        return roadmap

    @staticmethod
    def analyze_skill_gaps(user, target_career_path_id, current_skills_assessment):
        """Analyze skill gaps for a specific career path"""
        try:
            career_path = CareerPath.objects.get(id=target_career_path_id)
            required_skills = career_path.required_skills.all()
            recommended_skills = career_path.recommended_skills.all()

            # Prepare skills analysis
            skills_analysis = []
            for skill in required_skills:
                current_level = current_skills_assessment.get(str(skill.id), 'beginner')
                skills_analysis.append({
                    'skill_name': skill.name,
                    'required_level': skill.difficulty_level,
                    'current_level': current_level,
                    'is_required': True
                })

            for skill in recommended_skills:
                current_level = current_skills_assessment.get(str(skill.id), 'beginner')
                skills_analysis.append({
                    'skill_name': skill.name,
                    'recommended_level': skill.difficulty_level,
                    'current_level': current_level,
                    'is_required': False
                })

            prompt = f"""Analyze skill gaps for career: {career_path.title}

Skills Assessment:
{RoadmapAIService._format_skills_for_analysis(skills_analysis)}

Provide analysis:
1. Overall readiness score (0-100)
2. Critical skill gaps (high priority)
3. Areas of strength
4. Recommended next steps with timeline
5. Estimated preparation time
6. Confidence level assessment

Be specific and actionable."""

            ai_response = RoadmapAIService.call_huggingface_api(prompt)

            if ai_response:
                analysis = RoadmapAIService._parse_gap_analysis(ai_response, skills_analysis)
            else:
                analysis = RoadmapAIService._create_fallback_gap_analysis(skills_analysis)

            # Store skill assessments
            for skill_data in skills_analysis:
                skill = required_skills.filter(name=skill_data['skill_name']).first() or \
                        recommended_skills.filter(name=skill_data['skill_name']).first()

                if skill:
                    SkillAssessment.objects.update_or_create(
                        user=user,
                        skill=skill,
                        defaults={
                            'current_level': skill_data['current_level'],
                            'confidence_score': 70,
                            'assessment_method': 'self_assessment',
                            'skill_gaps': [gap['skill'] for gap in analysis.get('critical_gaps', [])],
                            'improvement_suggestions': [step['action'] for step in
                                                        analysis.get('recommended_next_steps', [])],
                            'next_learning_steps': analysis.get('recommended_next_steps', [])
                        }
                    )

            return analysis

        except Exception as e:
            print(f"Gap analysis failed: {str(e)}")
            return RoadmapAIService._create_fallback_gap_analysis([])

    @staticmethod
    def _format_skills_for_analysis(skills_analysis):
        """Format skills data for AI analysis"""
        formatted = []
        for skill in skills_analysis:
            status = "Required" if skill['is_required'] else "Recommended"
            formatted.append(
                f"- {skill['skill_name']}: Current: {skill['current_level']}, "
                f"Target: {skill.get('required_level', skill.get('recommended_level', 'intermediate'))} ({status})"
            )
        return '\n'.join(formatted)

    @staticmethod
    def _parse_gap_analysis(ai_response, skills_analysis):
        """Parse AI gap analysis response"""
        try:
            analysis = {
                'overall_readiness_score': 60,
                'critical_gaps': [],
                'strengths': [],
                'recommended_next_steps': [],
                'estimated_preparation_time': '6-8 months',
                'confidence_level': 'medium'
            }

            lines = ai_response.split('\n')

            # Extract readiness score
            for line in lines:
                if 'score' in line.lower() or '%' in line:
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        analysis['overall_readiness_score'] = min(100, int(numbers[0]))
                        break

            # Extract critical gaps
            gap_section = False
            for line in lines:
                line_lower = line.lower()
                if 'critical' in line_lower or 'gaps' in line_lower:
                    gap_section = True
                elif gap_section and line.strip():
                    if any(word in line_lower for word in ['strength', 'next', 'step', 'time']):
                        gap_section = False
                    else:
                        # Extract skill gap
                        skill_name = RoadmapAIService._extract_skill_from_line(line, skills_analysis)
                        if skill_name:
                            analysis['critical_gaps'].append({
                                'skill': skill_name,
                                'gap_severity': 'high',
                                'learning_priority': 8
                            })

            # Extract strengths
            strength_keywords = ['strength', 'good', 'strong', 'proficient']
            for line in lines:
                if any(keyword in line.lower() for keyword in strength_keywords):
                    clean_line = line.strip().replace('-', '').replace('*', '').strip()
                    if len(clean_line) > 10:
                        analysis['strengths'].append(clean_line)

            # Extract next steps
            step_keywords = ['next', 'recommend', 'should', 'action']
            for line in lines:
                if any(keyword in line.lower() for keyword in step_keywords):
                    clean_line = line.strip().replace('-', '').replace('*', '').strip()
                    if len(clean_line) > 10:
                        analysis['recommended_next_steps'].append({
                            'action': clean_line,
                            'timeline': '2-4 weeks',
                            'resources': ['Online courses', 'Practice projects']
                        })

            return analysis

        except Exception as e:
            print(f"Analysis parsing error: {str(e)}")
            return RoadmapAIService._create_fallback_gap_analysis(skills_analysis)

    @staticmethod
    def _extract_skill_from_line(line, skills_analysis):
        """Extract skill name from a line of text"""
        for skill in skills_analysis:
            if skill['skill_name'].lower() in line.lower():
                return skill['skill_name']
        return None

    @staticmethod
    def _create_fallback_gap_analysis(skills_analysis):
        """Create fallback gap analysis"""
        return {
            'overall_readiness_score': 60,
            'critical_gaps': [
                {
                    'skill': 'Technical Skills',
                    'current_level': 'beginner',
                    'required_level': 'intermediate',
                    'gap_severity': 'medium',
                    'learning_priority': 8
                }
            ],
            'strengths': ['Motivation to learn', 'Clear career goal'],
            'recommended_next_steps': [
                {
                    'action': 'Start with foundational courses',
                    'timeline': '2-3 months',
                    'resources': ['Online courses', 'Practice projects']
                }
            ],
            'estimated_preparation_time': '6-8 months',
            'confidence_level': 'medium'
        }

    @staticmethod
    def update_roadmap_progress(roadmap):
        """Update roadmap progress based on milestone completions"""
        try:
            milestones = roadmap.milestones.all()
            total_milestones = milestones.count()

            if total_milestones == 0:
                return roadmap

            completed_milestones = milestones.filter(status='completed')

            # Calculate overall progress
            progress = 0
            for milestone in milestones:
                if milestone.status == 'completed':
                    progress += 100
                elif milestone.status == 'in_progress':
                    progress += milestone.progress_percentage

            overall_progress = int(progress / total_milestones) if total_milestones > 0 else 0

            # Update roadmap
            roadmap.overall_progress_percentage = overall_progress
            roadmap.completed_milestones = [m.id for m in completed_milestones]

            # Check if roadmap should be completed
            if overall_progress == 100:
                roadmap.status = 'completed'

            roadmap.save()

            # Generate progress insights using AI
            insights = RoadmapAIService._generate_progress_insights(roadmap, overall_progress)

            return {
                'overall_progress': overall_progress,
                'completed_milestones': completed_milestones.count(),
                'total_milestones': total_milestones,
                'insights': insights,
                'status': roadmap.status
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def _generate_progress_insights(roadmap, progress_percentage):
        """Generate AI insights about learning progress"""
        try:
            prompt = f"""Analyze learning progress for: {roadmap.title}

Progress: {progress_percentage}%
Milestones: {roadmap.milestones.count()} total, {roadmap.milestones.filter(status='completed').count()} completed

Provide insights:
1. Performance assessment (excellent/good/needs improvement)
2. Key insights about progress pattern
3. Specific recommendations for improvement
4. Motivational message
5. Next focus areas
6. Estimated time to completion

Be encouraging and specific."""

            ai_response = RoadmapAIService.call_huggingface_api(prompt)

            if ai_response:
                return RoadmapAIService._parse_progress_insights(ai_response, progress_percentage)
            else:
                return RoadmapAIService._get_fallback_insights(progress_percentage)

        except Exception as e:
            return RoadmapAIService._get_fallback_insights(progress_percentage)

    @staticmethod
    def _parse_progress_insights(ai_response, progress_percentage):
        """Parse AI progress insights"""
        try:
            lines = ai_response.split('\n')

            insights = {
                'performance_assessment': 'good',
                'key_insights': [],
                'recommendations': [],
                'motivation_message': '',
                'next_focus_areas': [],
                'estimated_time_to_completion': '4-6 weeks'
            }

            # Extract performance assessment
            if progress_percentage >= 80:
                insights['performance_assessment'] = 'excellent'
            elif progress_percentage >= 50:
                insights['performance_assessment'] = 'good'
            else:
                insights['performance_assessment'] = 'needs_improvement'

            # Extract insights and recommendations
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if 'insight' in line.lower():
                    insights['key_insights'].append(line)
                elif 'recommend' in line.lower() or 'should' in line.lower():
                    insights['recommendations'].append(line)
                elif 'focus' in line.lower():
                    insights['next_focus_areas'].append(line.replace('Focus:', '').strip())
                elif len(line) > 50 and not insights['motivation_message']:
                    insights['motivation_message'] = line

            # Ensure we have content
            if not insights['key_insights']:
                insights['key_insights'] = ['Making progress on learning journey']
            if not insights['recommendations']:
                insights['recommendations'] = ['Continue consistent study schedule']
            if not insights['motivation_message']:
                insights['motivation_message'] = 'Keep up the great work on your learning journey!'

            return insights

        except Exception as e:
            return RoadmapAIService._get_fallback_insights(progress_percentage)

    @staticmethod
    def _get_fallback_insights(progress_percentage):
        """Generate fallback insights"""
        if progress_percentage >= 80:
            return {
                'performance_assessment': 'excellent',
                'key_insights': ['Great progress on your learning journey!'],
                'recommendations': ['Keep up the excellent work', 'Focus on completing remaining milestones'],
                'motivation_message': 'You\'re almost there! Your dedication is paying off.',
                'next_focus_areas': ['Final project completion', 'Skill consolidation'],
                'estimated_time_to_completion': '2-4 weeks'
            }
        elif progress_percentage >= 50:
            return {
                'performance_assessment': 'good',
                'key_insights': ['Steady progress on your roadmap'],
                'recommendations': ['Maintain consistent study schedule', 'Focus on practical application'],
                'motivation_message': 'You\'re making good progress. Stay consistent!',
                'next_focus_areas': ['Hands-on practice', 'Skill building'],
                'estimated_time_to_completion': '4-8 weeks'
            }
        else:
            return {
                'performance_assessment': 'needs_improvement',
                'key_insights': ['More consistent effort needed'],
                'recommendations': ['Set smaller daily goals', 'Find accountability partner'],
                'motivation_message': 'Every expert was once a beginner. Keep going!',
                'next_focus_areas': ['Foundation building', 'Consistent practice'],
                'estimated_time_to_completion': '8-12 weeks'
            }

    @staticmethod
    def recommend_learning_resources(user, skill_ids, learning_style='mixed', difficulty_level='intermediate'):
        """Recommend learning resources based on user preferences and skills"""
        try:
            skills = Skill.objects.filter(id__in=skill_ids)
            skills_names = [skill.name for skill in skills]

            prompt = f"""Recommend learning resources for: {', '.join(skills_names)}

Learning Style: {learning_style}
Difficulty: {difficulty_level}

Provide 5-8 high-quality resources including:
1. Resource title and description
2. Type (course/video/article/book/tutorial/project)
3. Estimated duration
4. Cost (free/paid)
5. Why it's recommended
6. Provider/platform

Also suggest a learning path and additional tips."""

            ai_response = RoadmapAIService.call_huggingface_api(prompt)

            if ai_response:
                recommendations = RoadmapAIService._parse_resource_recommendations(
                    ai_response, skills, skills_names, difficulty_level
                )
            else:
                recommendations = RoadmapAIService._create_fallback_resources(
                    skills_names, difficulty_level
                )

            # Store recommended resources in database
            RoadmapAIService._store_learning_resources(recommendations['resources'], skills)

            return recommendations

        except Exception as e:
            print(f"Resource recommendation failed: {str(e)}")
            return RoadmapAIService._create_fallback_resources(
                [skill.name for skill in Skill.objects.filter(id__in=skill_ids)],
                difficulty_level
            )

    @staticmethod
    def _parse_resource_recommendations(ai_response, skills, skills_names, difficulty_level):
        """Parse AI resource recommendations"""
        try:
            lines = ai_response.split('\n')
            resources = []

            current_resource = None
            resource_count = 0

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Look for resource titles (usually longer lines with certain patterns)
                if (len(line) > 15 and
                        (':' in line or 'course' in line.lower() or 'tutorial' in line.lower()) and
                        resource_count < 8):

                    if current_resource:
                        resources.append(current_resource)

                    title = line.split(':')[0].strip() if ':' in line else line

                    current_resource = {
                        'title': title,
                        'description': f'Learning resource for {", ".join(skills_names)}',
                        'url': 'https://example.com/resource',
                        'type': RoadmapAIService._determine_resource_type(line),
                        'difficulty': difficulty_level,
                        'estimated_duration': '2-4 hours',
                        'cost': 'free',
                        'provider': 'Online Platform',
                        'skills': skills_names,
                        'why_recommended': 'Matches your learning requirements'
                    }
                    resource_count += 1

                elif current_resource and len(line) > 20:
                    # Update description with more details
                    if 'free' in line.lower():
                        current_resource['cost'] = 'free'
                    elif 'paid' in line.lower():
                        current_resource['cost'] = 'paid'

                    if not current_resource['description'] or len(current_resource['description']) < 50:
                        current_resource['description'] = line

            # Add the last resource
            if current_resource:
                resources.append(current_resource)

            # Extract learning path and tips
            learning_path = f"Start with fundamentals of {skills_names[0] if skills_names else 'your chosen area'}, then progress to practical projects."
            tips = ['Practice regularly', 'Join online communities', 'Work on real projects',
                    'Seek feedback from peers']

            return {
                'resources': resources,
                'learning_path_suggestion': learning_path,
                'additional_tips': tips
            }

        except Exception as e:
            print(f"Resource parsing error: {str(e)}")
            return RoadmapAIService._create_fallback_resources(skills_names, difficulty_level)

    @staticmethod
    def _determine_resource_type(line):
        """Determine resource type from line content"""
        line_lower = line.lower()
        if 'course' in line_lower:
            return 'course'
        elif 'video' in line_lower:
            return 'video'
        elif 'article' in line_lower or 'blog' in line_lower:
            return 'article'
        elif 'book' in line_lower:
            return 'book'
        elif 'tutorial' in line_lower:
            return 'tutorial'
        elif 'project' in line_lower:
            return 'project'
        else:
            return 'course'  # Default

    @staticmethod
    def _store_learning_resources(resources, skills):
        """Store recommended resources in database"""
        for resource_data in resources:
            try:
                # Check if resource already exists
                existing_resource = LearningResource.objects.filter(
                    title=resource_data.get('title', '')[:100]  # Limit length
                ).first()

                if not existing_resource:
                    resource = LearningResource.objects.create(
                        title=resource_data.get('title', '')[:100],
                        description=resource_data.get('description', '')[:200],
                        url=resource_data.get('url', ''),
                        resource_type=resource_data.get('type', 'course'),
                        difficulty_level=resource_data.get('difficulty', 'intermediate'),
                        estimated_duration=resource_data.get('estimated_duration', ''),
                        cost=resource_data.get('cost', 'free'),
                        provider=resource_data.get('provider', '')[:50],
                        is_recommended=True
                    )

                    # Associate with skills
                    for skill in skills:
                        resource.skills.add(skill)

            except Exception as e:
                print(f"Error storing resource: {str(e)}")

    @staticmethod
    def _create_fallback_resources(skills_names, difficulty_level):
        """Create fallback resource recommendations"""
        return {
            'resources': [
                {
                    'title': f'Getting Started with {skills_names[0] if skills_names else "Your Skills"}',
                    'description': 'A comprehensive guide to get you started',
                    'url': 'https://example.com/guide',
                    'type': 'tutorial',
                    'difficulty': difficulty_level,
                    'estimated_duration': '2-4 hours',
                    'cost': 'free',
                    'provider': 'Community Resource',
                    'skills': skills_names,
                    'why_recommended': 'Great starting point for beginners'
                },
                {
                    'title': f'Advanced {skills_names[0] if skills_names else "Skills"} Course',
                    'description': 'Deep dive into advanced concepts',
                    'url': 'https://example.com/advanced',
                    'type': 'course',
                    'difficulty': 'advanced',
                    'estimated_duration': '4-6 weeks',
                    'cost': 'paid',
                    'provider': 'Online Learning Platform',
                    'skills': skills_names,
                    'why_recommended': 'Comprehensive coverage of advanced topics'
                }
            ],
            'learning_path_suggestion': f'Start with fundamentals, then move to practical projects in {skills_names[0] if skills_names else "your chosen area"}.',
            'additional_tips': ['Practice regularly', 'Join online communities', 'Work on real projects',
                                'Seek feedback']
        }
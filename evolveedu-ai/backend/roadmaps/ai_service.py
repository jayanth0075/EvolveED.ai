# roadmaps/ai_service.py
import openai
import json
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Skill, SkillCategory, CareerPath, PersonalizedRoadmap,
    RoadmapMilestone, SkillAssessment, LearningResource
)

openai.api_key = settings.OPENAI_API_KEY


class RoadmapAIService:

    @staticmethod
    def generate_personalized_roadmap(user, career_goal, current_skills, experience_level,
                                      time_commitment, target_months, learning_style, focus_areas):
        """Generate a personalized learning roadmap using AI"""
        try:
            # Prepare context for AI
            current_skills_str = ", ".join(current_skills) if current_skills else "None specified"
            focus_areas_str = ", ".join(focus_areas) if focus_areas else "General development"

            prompt = f"""
            Create a personalized learning roadmap for someone who wants to achieve: "{career_goal}"

            Current Skills: {current_skills_str}
            Experience Level: {experience_level}
            Time Commitment: {time_commitment} hours per week
            Target Timeline: {target_months} months
            Learning Style: {learning_style}
            Focus Areas: {focus_areas_str}

            Generate a structured roadmap with the following JSON format:
            {{
                "roadmap_title": "...",
                "description": "...",
                "estimated_total_hours": number,
                "milestones": [
                    {{
                        "title": "...",
                        "description": "...",
                        "skill_name": "...",
                        "estimated_hours": number,
                        "learning_resources": [
                            {{"type": "course", "title": "...", "url": "...", "description": "..."}},
                            {{"type": "project", "title": "...", "description": "..."}}
                        ],
                        "practice_tasks": ["task1", "task2", ...],
                        "completion_criteria": ["criteria1", "criteria2", ...],
                        "order": number
                    }}
                ],
                "weekly_goals": [
                    {{"week": 1, "goal": "...", "focus_skills": ["skill1", "skill2"]}},
                    {{"week": 2, "goal": "...", "focus_skills": ["skill1", "skill2"]}}
                ],
                "personalized_recommendations": [
                    "recommendation1",
                    "recommendation2"
                ]
            }}

            Ensure milestones are progressive, realistic for the given timeframe, and tailored to the learning style.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an expert career counselor and learning path designer. Generate comprehensive, realistic learning roadmaps."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.8
            )

            ai_roadmap = json.loads(response.choices[0].message.content)

            # Create the roadmap in database
            roadmap = PersonalizedRoadmap.objects.create(
                user=user,
                title=ai_roadmap['roadmap_title'],
                description=ai_roadmap['description'],
                start_date=timezone.now().date(),
                target_completion_date=timezone.now().date() + timedelta(days=target_months * 30),
                estimated_hours_per_week=time_commitment,
                status='active',
                personalized_recommendations=ai_roadmap.get('personalized_recommendations', []),
                weekly_goals=ai_roadmap.get('weekly_goals', [])
            )

            # Create milestones
            for milestone_data in ai_roadmap['milestones']:
                # Find or create skill
                skill_name = milestone_data.get('skill_name', 'General Skill')
                skill, created = Skill.objects.get_or_create(
                    name=skill_name,
                    defaults={
                        'description': f'Skill related to {skill_name}',
                        'category': SkillCategory.objects.first() or SkillCategory.objects.create(name='General'),
                        'difficulty_level': experience_level,
                        'estimated_hours': milestone_data.get('estimated_hours', 10)
                    }
                )

                RoadmapMilestone.objects.create(
                    roadmap=roadmap,
                    title=milestone_data['title'],
                    description=milestone_data['description'],
                    skill=skill,
                    learning_resources=milestone_data.get('learning_resources', []),
                    practice_tasks=milestone_data.get('practice_tasks', []),
                    completion_criteria=milestone_data.get('completion_criteria', []),
                    estimated_hours=milestone_data.get('estimated_hours', 10),
                    order=milestone_data.get('order', 1)
                )

            return roadmap

        except Exception as e:
            # Fallback: create basic roadmap
            return RoadmapAIService._create_fallback_roadmap(
                user, career_goal, target_months, time_commitment
            )

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
                'hours': target_months * time_commitment * 0.3
            },
            {
                'title': 'Intermediate Development',
                'description': 'Develop intermediate level competencies',
                'hours': target_months * time_commitment * 0.4
            },
            {
                'title': 'Advanced Practice',
                'description': 'Advanced skills and real-world application',
                'hours': target_months * time_commitment * 0.3
            }
        ]

        general_category = SkillCategory.objects.first() or SkillCategory.objects.create(name='General')

        for i, milestone in enumerate(basic_milestones):
            skill, created = Skill.objects.get_or_create(
                name=f"{career_goal} - {milestone['title']}",
                defaults={
                    'description': milestone['description'],
                    'category': general_category,
                    'estimated_hours': int(milestone['hours'])
                }
            )

            RoadmapMilestone.objects.create(
                roadmap=roadmap,
                title=milestone['title'],
                description=milestone['description'],
                skill=skill,
                estimated_hours=int(milestone['hours']),
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

            prompt = f"""
            Analyze skill gaps for someone targeting the career path: "{career_path.title}"

            Skills Analysis:
            {json.dumps(skills_analysis, indent=2)}

            Provide analysis in JSON format:
            {{
                "overall_readiness_score": number (0-100),
                "critical_gaps": [
                    {{
                        "skill": "...",
                        "current_level": "...",
                        "required_level": "...",
                        "gap_severity": "high|medium|low",
                        "learning_priority": number (1-10)
                    }}
                ],
                "strengths": ["strength1", "strength2", ...],
                "recommended_next_steps": [
                    {{
                        "action": "...",
                        "timeline": "...",
                        "resources": ["resource1", "resource2"]
                    }}
                ],
                "estimated_preparation_time": "X months",
                "confidence_level": "high|medium|low"
            }}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an expert career analyst. Provide detailed skill gap analysis with actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            analysis = json.loads(response.choices[0].message.content)

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
                            'confidence_score': 70,  # Default confidence
                            'assessment_method': 'self_assessment',
                            'skill_gaps': [gap['skill'] for gap in analysis.get('critical_gaps', [])],
                            'improvement_suggestions': [step['action'] for step in
                                                        analysis.get('recommended_next_steps', [])],
                            'next_learning_steps': analysis.get('recommended_next_steps', [])
                        }
                    )

            return analysis

        except Exception as e:
            # Fallback analysis
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
            in_progress_milestones = milestones.filter(status='in_progress')

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
            milestones_data = []
            for milestone in roadmap.milestones.all():
                milestones_data.append({
                    'title': milestone.title,
                    'status': milestone.status,
                    'progress': milestone.progress_percentage,
                    'hours_spent': milestone.actual_hours_spent,
                    'estimated_hours': milestone.estimated_hours
                })

            prompt = f"""
            Analyze learning progress for roadmap: "{roadmap.title}"
            Overall Progress: {progress_percentage}%

            Milestones Status:
            {json.dumps(milestones_data, indent=2)}

            Provide insights in JSON format:
            {{
                "performance_assessment": "excellent|good|needs_improvement|concerning",
                "key_insights": ["insight1", "insight2", ...],
                "recommendations": ["recommendation1", "recommendation2", ...],
                "motivation_message": "...",
                "next_focus_areas": ["area1", "area2", ...],
                "estimated_time_to_completion": "X weeks/months"
            }}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are a supportive learning coach providing progress insights and motivation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.8
            )

            return json.loads(response.choices[0].message.content)

        except:
            # Fallback insights
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

            prompt = f"""
            Recommend learning resources for these skills: {', '.join(skills_names)}

            User Preferences:
            - Learning Style: {learning_style}
            - Difficulty Level: {difficulty_level}

            Provide recommendations in JSON format:
            {{
                "resources": [
                    {{
                        "title": "...",
                        "description": "...",
                        "url": "https://...",
                        "type": "course|video|article|book|tutorial|project",
                        "difficulty": "beginner|intermediate|advanced",
                        "estimated_duration": "...",
                        "cost": "free|paid",
                        "provider": "...",
                        "skills": ["skill1", "skill2"],
                        "why_recommended": "..."
                    }}
                ],
                "learning_path_suggestion": "...",
                "additional_tips": ["tip1", "tip2", ...]
            }}

            Focus on high-quality, practical resources. Include a mix of free and paid options.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an expert learning resource curator. Recommend high-quality, practical learning materials."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            recommendations = json.loads(response.choices[0].message.content)

            # Store recommended resources in database
            for resource_data in recommendations.get('resources', []):
                # Check if resource already exists
                existing_resource = LearningResource.objects.filter(
                    url=resource_data.get('url', ''),
                    title=resource_data.get('title', '')
                ).first()

                if not existing_resource:
                    resource = LearningResource.objects.create(
                        title=resource_data.get('title', ''),
                        description=resource_data.get('description', ''),
                        url=resource_data.get('url', ''),
                        resource_type=resource_data.get('type', 'course'),
                        difficulty_level=resource_data.get('difficulty', difficulty_level),
                        estimated_duration=resource_data.get('estimated_duration', ''),
                        cost=resource_data.get('cost', 'free'),
                        provider=resource_data.get('provider', ''),
                        is_recommended=True
                    )

                    # Associate with skills
                    for skill_name in resource_data.get('skills', []):
                        skill = skills.filter(name__icontains=skill_name).first()
                        if skill:
                            resource.skills.add(skill)

            return recommendations

        except Exception as e:
            # Fallback recommendations
            return {
                'resources': [
                    {
                        'title': 'Getting Started Guide',
                        'description': 'A comprehensive guide to get you started',
                        'url': 'https://example.com/guide',
                        'type': 'tutorial',
                        'difficulty': difficulty_level,
                        'estimated_duration': '2-4 hours',
                        'cost': 'free',
                        'provider': 'Community Resource',
                        'skills': skills_names,
                        'why_recommended': 'Great starting point for beginners'
                    }
                ],
                'learning_path_suggestion': f'Start with fundamentals, then move to practical projects in {skills_names[0] if skills_names else "your chosen area"}.',
                'additional_tips': ['Practice regularly', 'Join online communities', 'Work on real projects']
            }
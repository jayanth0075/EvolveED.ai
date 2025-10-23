# tutor/ai_service.py
import requests
import json
import time
import re
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from .models import TutorSession, ChatMessage, ProblemSolvingSession, ConceptExplanation, StudyPlan, LearningInsight


class TutorAIService:

    @staticmethod
    def call_huggingface_api(prompt, max_retries=3, delay=1):
        """Make API call to Hugging Face with retry logic"""
        headers = {
            "Authorization": f"Bearer {getattr(settings, 'HUGGINGFACE_API_KEY', '')}",
            "Content-Type": "application/json"
        }

        # Using conversational model for tutoring
        api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False,
                "pad_token_id": 50256
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
    def generate_tutor_response(session, user_message, include_context=True, request_explanation=False,
                                request_examples=False):
        """Generate AI tutor response based on user message and context"""
        try:
            # Build conversation context
            context = ""
            if include_context:
                recent_messages = session.messages.order_by('-timestamp')[:5]
                for msg in reversed(recent_messages):
                    role = "Student" if msg.message_type == "user" else "Tutor"
                    context += f"{role}: {msg.content}\n"

            # Build tutoring prompt
            tutor_prompt = TutorAIService._build_tutor_prompt(
                session, user_message, context, request_explanation, request_examples
            )

            # Generate response
            start_time = timezone.now()
            ai_response = TutorAIService.call_huggingface_api(tutor_prompt)
            end_time = timezone.now()

            response_time = int((end_time - start_time).total_seconds() * 1000)

            if ai_response:
                tutor_response = TutorAIService._clean_tutor_response(ai_response)
            else:
                tutor_response = TutorAIService._generate_fallback_response(user_message, session.session_type)

            # Analyze the message
            intent, confidence, topics = TutorAIService._analyze_message_content(user_message)

            # Save user message
            user_msg = ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=user_message,
                intent=intent,
                confidence_score=confidence,
                topic_tags=topics
            )

            # Save tutor response
            tutor_msg = ChatMessage.objects.create(
                session=session,
                message_type='tutor',
                content=tutor_response,
                response_time_ms=response_time
            )

            # Update session activity
            session.last_activity = timezone.now()
            session.save()

            return {
                'response': tutor_response,
                'message_id': tutor_msg.id,
                'response_time_ms': response_time,
                'intent': intent,
                'topics': topics
            }

        except Exception as e:
            print(f"Tutor response generation failed: {str(e)}")
            # Fallback response
            fallback_response = TutorAIService._generate_fallback_response(user_message, session.session_type)

            # Save messages even with fallback
            ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=user_message
            )

            tutor_msg = ChatMessage.objects.create(
                session=session,
                message_type='tutor',
                content=fallback_response
            )

            return {
                'response': fallback_response,
                'message_id': tutor_msg.id,
                'error': str(e)
            }

    @staticmethod
    def _build_tutor_prompt(session, user_message, context, request_explanation=False, request_examples=False):
        """Build tutoring prompt for AI"""
        subject_info = f" in {session.subject}" if session.subject else ""
        level_info = f" at {session.difficulty_level} level" if session.difficulty_level else ""

        base_prompt = f"""You are a helpful AI tutor{subject_info}. You're teaching a student{level_info}.

Your teaching style:
- Be encouraging and patient
- Ask guiding questions to promote learning
- Provide clear, step-by-step explanations
- Use examples when helpful
- Check understanding frequently

Session type: {session.get_session_type_display()}

Previous conversation:
{context}

Student: {user_message}

Tutor:"""

        if session.session_type == 'problem_solving':
            base_prompt += """
Focus on:
- Breaking problems into steps
- Teaching problem-solving strategies  
- Providing hints rather than direct answers initially
- Encouraging critical thinking"""

        elif session.session_type == 'concept_explanation':
            base_prompt += """
Focus on:
- Clear, simple explanations
- Real-world examples
- Building from basic to complex
- Checking understanding"""

        if request_explanation:
            base_prompt += "\nThe student specifically needs a detailed explanation."

        if request_examples:
            base_prompt += "\nThe student is requesting examples to illustrate the concept."

        return base_prompt

    @staticmethod
    def _clean_tutor_response(ai_response):
        """Clean and format AI response for tutoring"""
        if not ai_response:
            return "I'm here to help you learn! Could you please clarify your question?"

        # Remove any unwanted prefixes
        response = ai_response.strip()

        # Remove common AI artifacts
        prefixes_to_remove = ['Tutor:', 'AI:', 'Assistant:', 'Response:']
        for prefix in prefixes_to_remove:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()

        # Ensure response is not too long
        if len(response) > 800:
            sentences = response.split('.')
            response = '. '.join(sentences[:4]) + '.'

        # Ensure response is helpful
        if len(response) < 20:
            response = "That's a great question! Let me help you understand this concept better. Could you provide a bit more detail about what you'd like to learn?"

        return response

    @staticmethod
    def _analyze_message_content(message):
        """Analyze user message to extract intent, confidence, and topics"""
        # Simple analysis without external API
        message_lower = message.lower()

        # Determine intent
        intent = 'general'
        if any(word in message_lower for word in ['what', 'how', 'why', 'when', 'where']):
            intent = 'question'
        elif any(word in message_lower for word in ['explain', 'tell me', 'help me understand']):
            intent = 'explanation_request'
        elif any(word in message_lower for word in ['problem', 'solve', 'calculate', 'find']):
            intent = 'problem_help'
        elif any(word in message_lower for word in ['clarify', 'confused', 'don\'t understand']):
            intent = 'clarification'

        # Simple confidence based on message characteristics
        confidence = 0.5
        if len(message) > 50:
            confidence += 0.2
        if '?' in message:
            confidence += 0.1
        if any(word in message_lower for word in ['specific', 'exactly', 'precisely']):
            confidence += 0.2

        confidence = min(1.0, confidence)

        # Extract basic topics (simple keyword extraction)
        topics = []
        academic_terms = [
            'math', 'mathematics', 'science', 'physics', 'chemistry', 'biology',
            'history', 'literature', 'english', 'programming', 'computer',
            'economics', 'psychology', 'philosophy', 'art', 'music', 'language'
        ]

        for term in academic_terms:
            if term in message_lower:
                topics.append(term)

        return intent, confidence, topics[:3]  # Limit to 3 topics

    @staticmethod
    def _generate_fallback_response(user_message, session_type):
        """Generate fallback response when AI service fails"""
        responses = {
            'chat': "I understand you're asking about that topic. Let me help you work through this step by step. Could you provide a bit more detail about what specifically you'd like to understand?",
            'problem_solving': "I see you have a problem to solve. Let's break this down together. Can you share the specific problem statement or what part you're finding challenging?",
            'concept_explanation': "That's a great concept to explore! Let me help you understand this better. What specific aspect would you like me to explain first?",
            'homework_help': "I'm here to help you with your homework. Let's work through this together. What subject area are we focusing on?",
            'exam_prep': "Exam preparation is important! I can help you review key concepts and practice problems. What topics would you like to focus on?"
        }

        return responses.get(session_type, "I'm here to help you learn! How can I assist you today?")

    @staticmethod
    def solve_problem(problem_session):
        """AI-powered problem solving with step-by-step guidance"""
        try:
            problem = problem_session.problem_statement
            problem_type = problem_session.problem_type
            difficulty = problem_session.difficulty_level

            prompt = f"""Solve this {problem_type} problem step by step:

Problem: {problem}
Difficulty: {difficulty}

Provide:
1. Problem analysis - what are we asked to find?
2. Step-by-step solution with clear explanations
3. Final answer
4. Key concepts used
5. Similar practice problems

Be educational and show your work clearly."""

            ai_response = TutorAIService.call_huggingface_api(prompt)

            if ai_response:
                solution_data = TutorAIService._parse_problem_solution(ai_response, problem_type)
            else:
                solution_data = TutorAIService._create_fallback_solution(problem, problem_type)

            # Update problem session
            problem_session.solution_steps = solution_data.get('solution_steps', [])
            problem_session.final_answer = solution_data.get('final_answer', '')
            problem_session.explanation = solution_data.get('explanation', '')
            problem_session.key_concepts = solution_data.get('key_concepts', [])
            problem_session.similar_problems = solution_data.get('similar_problems', [])
            problem_session.learning_resources = solution_data.get('learning_resources', [])
            problem_session.status = 'completed'
            problem_session.save()

            return solution_data

        except Exception as e:
            print(f"Problem solving failed: {str(e)}")
            return TutorAIService._create_fallback_solution(problem_session.problem_statement,
                                                            problem_session.problem_type)

    @staticmethod
    def _parse_problem_solution(ai_response, problem_type):
        """Parse AI problem solution response"""
        try:
            lines = ai_response.split('\n')

            solution_data = {
                'analysis': '',
                'solution_steps': [],
                'final_answer': '',
                'explanation': '',
                'key_concepts': [],
                'similar_problems': [],
                'learning_resources': []
            }

            current_section = None
            step_number = 0

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                line_lower = line.lower()

                # Identify sections
                if 'analysis' in line_lower or 'understand' in line_lower:
                    current_section = 'analysis'
                    if not solution_data['analysis']:
                        solution_data['analysis'] = line
                elif 'step' in line_lower or 'solution' in line_lower:
                    current_section = 'steps'
                elif 'answer' in line_lower or 'result' in line_lower:
                    current_section = 'answer'
                    if 'final' in line_lower and not solution_data['final_answer']:
                        solution_data['final_answer'] = line
                elif 'concept' in line_lower:
                    current_section = 'concepts'
                elif 'similar' in line_lower or 'practice' in line_lower:
                    current_section = 'similar'

                # Parse content based on current section
                if current_section == 'steps' and len(line) > 10:
                    if any(keyword in line_lower for keyword in ['step', 'first', 'next', 'then', 'finally']):
                        step_number += 1
                        solution_data['solution_steps'].append({
                            'step': step_number,
                            'description': line,
                            'work': line
                        })
                elif current_section == 'concepts' and len(line) > 5:
                    concept = line.replace('-', '').replace('*', '').strip()
                    if concept and concept not in solution_data['key_concepts']:
                        solution_data['key_concepts'].append(concept)
                elif current_section == 'similar' and len(line) > 15:
                    solution_data['similar_problems'].append({
                        'problem': line,
                        'difficulty': 'medium'
                    })

            # Ensure we have basic content
            if not solution_data['analysis']:
                solution_data['analysis'] = f'This is a {problem_type} problem that requires systematic approach.'

            if not solution_data['solution_steps']:
                solution_data['solution_steps'] = [
                    {'step': 1, 'description': 'Analyze the problem', 'work': 'Identify known and unknown variables'},
                    {'step': 2, 'description': 'Apply relevant concepts',
                     'work': 'Use appropriate formulas or methods'},
                    {'step': 3, 'description': 'Calculate result', 'work': 'Perform calculations step by step'}
                ]

            if not solution_data['explanation']:
                solution_data['explanation'] = ai_response[:200] + '...' if len(ai_response) > 200 else ai_response

            solution_data['learning_resources'] = [
                {'title': f'{problem_type.capitalize()} Tutorial', 'type': 'tutorial',
                 'url': 'https://example.com/tutorial'}
            ]

            return solution_data

        except Exception as e:
            print(f"Solution parsing error: {str(e)}")
            return TutorAIService._create_fallback_solution('', problem_type)

    @staticmethod
    def _create_fallback_solution(problem, problem_type):
        """Create fallback solution when AI fails"""
        return {
            'analysis': f'This is a {problem_type} problem that requires systematic approach.',
            'solution_steps': [
                {'step': 1, 'description': 'Analyze the problem', 'work': 'Identify known and unknown variables'},
                {'step': 2, 'description': 'Apply relevant concepts', 'work': 'Use appropriate formulas or methods'},
                {'step': 3, 'description': 'Calculate result', 'work': 'Perform calculations step by step'}
            ],
            'final_answer': 'Please provide more specific problem details for accurate solution',
            'explanation': 'A systematic approach helps solve problems effectively.',
            'key_concepts': [problem_type, 'problem-solving'],
            'similar_problems': [
                {'problem': f'Practice {problem_type} problem 1', 'difficulty': 'easy'},
                {'problem': f'Practice {problem_type} problem 2', 'difficulty': 'medium'}
            ],
            'learning_resources': [
                {'title': f'{problem_type.capitalize()} Guide', 'type': 'tutorial', 'url': 'https://example.com/guide'}
            ]
        }

    @staticmethod
    def explain_concept(concept_explanation):
        """Generate comprehensive concept explanation"""
        try:
            concept = concept_explanation.concept_name
            subject = concept_explanation.subject_area
            request = concept_explanation.explanation_request

            prompt = f"""Explain the concept: "{concept}" in {subject}

Student's request: {request}

Provide a comprehensive explanation including:
1. Clear definition
2. 3 real-world examples
3. Helpful analogies
4. Prerequisites needed
5. Related concepts
6. Practice questions

Make it educational and easy to understand."""

            ai_response = TutorAIService.call_huggingface_api(prompt)

            if ai_response:
                explanation_data = TutorAIService._parse_concept_explanation(ai_response, concept, subject)
            else:
                explanation_data = TutorAIService._create_fallback_explanation(concept, subject)

            # Update concept explanation
            concept_explanation.explanation = explanation_data.get('explanation', '')
            concept_explanation.examples = explanation_data.get('examples', [])
            concept_explanation.analogies = explanation_data.get('analogies', [])
            concept_explanation.prerequisites = explanation_data.get('prerequisites', [])
            concept_explanation.related_concepts = explanation_data.get('related_concepts', [])
            concept_explanation.practice_questions = explanation_data.get('practice_questions', [])
            concept_explanation.visual_aids = explanation_data.get('visual_aids', [])
            concept_explanation.save()

            return explanation_data

        except Exception as e:
            print(f"Concept explanation failed: {str(e)}")
            return TutorAIService._create_fallback_explanation(
                concept_explanation.concept_name,
                concept_explanation.subject_area
            )

    @staticmethod
    def _parse_concept_explanation(ai_response, concept, subject):
        """Parse AI concept explanation response"""
        try:
            lines = ai_response.split('\n')

            explanation_data = {
                'explanation': '',
                'examples': [],
                'analogies': [],
                'prerequisites': [],
                'related_concepts': [],
                'practice_questions': [],
                'visual_aids': []
            }

            current_section = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                line_lower = line.lower()

                # Identify sections
                if 'definition' in line_lower or 'explanation' in line_lower:
                    current_section = 'explanation'
                    if not explanation_data['explanation']:
                        explanation_data['explanation'] = line
                elif 'example' in line_lower:
                    current_section = 'examples'
                elif 'analogy' in line_lower or 'like' in line_lower:
                    current_section = 'analogies'
                elif 'prerequisite' in line_lower or 'need to know' in line_lower:
                    current_section = 'prerequisites'
                elif 'related' in line_lower or 'similar' in line_lower:
                    current_section = 'related'
                elif 'question' in line_lower or 'practice' in line_lower:
                    current_section = 'questions'

                # Parse content based on current section
                if current_section == 'examples' and len(line) > 15:
                    explanation_data['examples'].append({
                        'title': f'Example {len(explanation_data["examples"]) + 1}',
                        'description': line,
                        'context': 'practical application'
                    })
                elif current_section == 'analogies' and len(line) > 15:
                    explanation_data['analogies'].append({
                        'analogy': line,
                        'explanation': f'This helps understand {concept}'
                    })
                elif current_section == 'prerequisites' and len(line) > 5:
                    prereq = line.replace('-', '').replace('*', '').strip()
                    if prereq:
                        explanation_data['prerequisites'].append(prereq)
                elif current_section == 'related' and len(line) > 5:
                    related = line.replace('-', '').replace('*', '').strip()
                    if related:
                        explanation_data['related_concepts'].append(related)
                elif current_section == 'questions' and '?' in line:
                    explanation_data['practice_questions'].append({
                        'question': line,
                        'difficulty': 'medium'
                    })

            # Ensure we have basic content
            if not explanation_data['explanation']:
                explanation_data[
                    'explanation'] = f'{concept} is an important concept in {subject} that involves understanding key principles and applications.'

            # Fill missing examples
            if not explanation_data['examples']:
                explanation_data['examples'] = [
                    {'title': 'Basic Example', 'description': f'A simple example of {concept}',
                     'context': 'everyday situation'},
                    {'title': 'Advanced Example', 'description': f'A complex application of {concept}',
                     'context': 'professional context'}
                ]

            # Fill missing analogies
            if not explanation_data['analogies']:
                explanation_data['analogies'] = [
                    {'analogy': f'{concept} is like a building block',
                     'explanation': 'It forms the foundation for understanding more complex ideas'}
                ]

            # Add visual aids suggestions
            explanation_data['visual_aids'] = [
                {'type': 'diagram', 'description': f'Visual representation of {concept}',
                 'suggestion': 'Create a concept map'},
                {'type': 'chart', 'description': f'{concept} examples chart', 'suggestion': 'Make a comparison table'}
            ]

            return explanation_data

        except Exception as e:
            print(f"Explanation parsing error: {str(e)}")
            return TutorAIService._create_fallback_explanation(concept, subject)

    @staticmethod
    def _create_fallback_explanation(concept, subject):
        """Create fallback explanation when AI fails"""
        return {
            'explanation': f'{concept} is an important concept in {subject} that requires understanding of fundamental principles.',
            'examples': [
                {'title': 'Basic Example', 'description': f'A simple example of {concept}',
                 'context': 'everyday situation'},
                {'title': 'Advanced Example', 'description': f'A more complex application of {concept}',
                 'context': 'professional context'}
            ],
            'analogies': [
                {'analogy': f'{concept} is like a foundation', 'explanation': 'It supports more complex understanding'}
            ],
            'prerequisites': ['basic foundation knowledge'],
            'related_concepts': [f'concepts related to {concept}'],
            'practice_questions': [
                {'question': f'What is the main principle behind {concept}?', 'difficulty': 'easy'},
                {'question': f'How would you apply {concept} in real situations?', 'difficulty': 'medium'}
            ],
            'visual_aids': [
                {'type': 'diagram', 'description': f'Visual representation of {concept}',
                 'suggestion': 'Create a simple diagram'}
            ]
        }

    @staticmethod
    def generate_study_plan(plan_data):
        """Generate AI-powered personalized study plan"""
        try:
            prompt = f"""Create a comprehensive study plan:

Subject: {plan_data['subject']}
Topics: {', '.join(plan_data['topics'])}
Duration: {plan_data['duration_days']} days
Daily study time: {plan_data['daily_study_time']} minutes
Difficulty: {plan_data['difficulty_level']}
Learning style: {plan_data['learning_style']}
Goals: {', '.join(plan_data.get('goals', []))}

Create a detailed day-by-day study schedule with:
- Daily tasks and topics
- Study milestones
- Resource recommendations
- Progress tracking methods

Make it practical and achievable."""

            ai_response = TutorAIService.call_huggingface_api(prompt)

            if ai_response:
                return TutorAIService._parse_study_plan(ai_response, plan_data)
            else:
                return TutorAIService._create_fallback_study_plan(plan_data)

        except Exception as e:
            print(f"Study plan generation failed: {str(e)}")
            return TutorAIService._create_fallback_study_plan(plan_data)

    @staticmethod
    def _parse_study_plan(ai_response, plan_data):
        """Parse AI study plan response"""
        try:
            duration = plan_data['duration_days']
            daily_time = plan_data['daily_study_time']
            topics = plan_data['topics']

            # Create basic schedule structure
            schedule = {}
            topics_per_day = max(1, len(topics) // duration)
            current_topics = topics.copy()

            lines = ai_response.split('\n')
            day_pattern = re.compile(r'day\s*(\d+)', re.IGNORECASE)

            current_day = 0

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Look for day patterns
                day_match = day_pattern.search(line)
                if day_match:
                    current_day = int(day_match.group(1))
                    if current_day <= duration:
                        day_topics = current_topics[:topics_per_day] if current_topics else [
                            topics[0] if topics else 'Review']
                        current_topics = current_topics[topics_per_day:]

                        schedule[f"day_{current_day}"] = {
                            "topics": day_topics,
                            "tasks": [
                                {"task": f"Study {topic}", "duration_minutes": daily_time // len(day_topics),
                                 "type": "reading"}
                                for topic in day_topics
                            ],
                            "goals": [f"Understand {topic}" for topic in day_topics]
                        }

            # Fill remaining days if needed
            for day in range(1, duration + 1):
                if f"day_{day}" not in schedule:
                    remaining_topics = topics[day % len(topics):day % len(topics) + 1] if topics else ['General Review']
                    schedule[f"day_{day}"] = {
                        "topics": remaining_topics,
                        "tasks": [
                            {"task": f"Study {remaining_topics[0]}", "duration_minutes": daily_time, "type": "review"}
                        ],
                        "goals": [f"Review {remaining_topics[0]}"]
                    }

            return {
                "study_schedule": schedule,
                "milestones": [
                    {"day": duration // 2, "milestone": "Mid-point review", "assessment": "Review progress"},
                    {"day": duration, "milestone": "Complete study plan", "assessment": "Final assessment"}
                ],
                "resources": [
                    {"title": "Study Guide", "type": "website", "url": "", "topics": topics}
                ],
                "total_tasks": sum(len(day_data["tasks"]) for day_data in schedule.values()),
                "study_tips": ["Study consistently", "Take regular breaks", "Review frequently", "Practice actively"]
            }

        except Exception as e:
            print(f"Study plan parsing error: {str(e)}")
            return TutorAIService._create_fallback_study_plan(plan_data)

    @staticmethod
    def _create_fallback_study_plan(plan_data):
        """Create fallback study plan when AI fails"""
        duration = plan_data['duration_days']
        daily_time = plan_data['daily_study_time']
        topics = plan_data['topics']

        # Create basic schedule
        schedule = {}
        topics_per_day = max(1, len(topics) // duration)

        for day in range(1, duration + 1):
            day_topics = topics[:topics_per_day]
            topics = topics[topics_per_day:] + topics[:topics_per_day]  # Rotate topics

            if not day_topics:
                day_topics = [plan_data['subject'] or 'General Study']

            schedule[f"day_{day}"] = {
                "topics": day_topics,
                "tasks": [
                    {"task": f"Study {topic}", "duration_minutes": daily_time // len(day_topics), "type": "reading"}
                    for topic in day_topics
                ],
                "goals": [f"Understand {topic}" for topic in day_topics]
            }

        return {
            "study_schedule": schedule,
            "milestones": [
                {"day": duration // 2, "milestone": "Mid-point review", "assessment": "Review progress"},
                {"day": duration, "milestone": "Complete study plan", "assessment": "Final assessment"}
            ],
            "resources": [
                {"title": "Study Guide", "type": "website", "url": "", "topics": plan_data['topics']}
            ],
            "total_tasks": sum(len(day_data["tasks"]) for day_data in schedule.values()),
            "study_tips": ["Study consistently", "Take breaks", "Review regularly", "Practice actively"]
        }

    @staticmethod
    def generate_learning_insights(user):
        """Generate personalized learning insights based on user activity"""
        try:
            # Collect user data
            sessions = TutorSession.objects.filter(user=user).order_by('-started_at')[:20]

            if sessions.count() < 3:
                return []

            insights = []

            # Study frequency insight
            session_dates = [s.started_at.date() for s in sessions]
            unique_dates = set(session_dates)

            if len(unique_dates) >= 5:
                avg_gap = TutorAIService._calculate_average_session_gap(sessions)
                if avg_gap > 7:
                    insights.append({
                        'type': 'pattern',
                        'title': 'Study Frequency Pattern',
                        'description': f'You typically have {avg_gap:.1f} days between study sessions. More frequent sessions could improve retention.',
                        'priority': 'medium',
                        'actions': ['Schedule regular study times', 'Set daily learning goals']
                    })

            # Subject preference insight
            subject_counts = {}
            for session in sessions:
                if session.subject:
                    subject_counts[session.subject] = subject_counts.get(session.subject, 0) + 1

            if subject_counts:
                favorite_subject = max(subject_counts, key=subject_counts.get)
                insights.append({
                    'type': 'strength',
                    'title': 'Subject Preference',
                    'description': f'You show strong engagement with {favorite_subject}. Consider exploring advanced topics in this area.',
                    'priority': 'low',
                    'actions': [f'Explore advanced {favorite_subject} topics', 'Share knowledge with others']
                })

            # Session duration insight
            avg_duration = sum(s.duration_minutes or 0 for s in sessions) / sessions.count()
            if avg_duration < 15:
                insights.append({
                    'type': 'improvement',
                    'title': 'Session Duration',
                    'description': f'Your average session is {avg_duration:.1f} minutes. Longer sessions might improve learning depth.',
                    'priority': 'medium',
                    'actions': ['Plan longer study sessions', 'Set session goals before starting']
                })

            # Create insight objects
            for insight_data in insights:
                LearningInsight.objects.create(
                    user=user,
                    insight_type=insight_data['type'],
                    title=insight_data['title'],
                    description=insight_data['description'],
                    priority_level=insight_data['priority'],
                    suggested_actions=insight_data['actions'],
                    confidence_score=0.8
                )

            return insights

        except Exception as e:
            print(f"Learning insights generation failed: {str(e)}")
            return []

    @staticmethod
    def _calculate_average_session_gap(sessions):
        """Calculate average days between study sessions"""
        if len(sessions) < 2:
            return 0

        gaps = []
        for i in range(len(sessions) - 1):
            gap = (sessions[i].started_at.date() - sessions[i + 1].started_at.date()).days
            gaps.append(gap)

        return sum(gaps) / len(gaps) if gaps else 0
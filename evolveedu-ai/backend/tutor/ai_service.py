# tutor/ai_service.py
import openai
import json
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from .models import TutorSession, ChatMessage, ProblemSolvingSession, ConceptExplanation, StudyPlan, LearningInsight

openai.api_key = settings.OPENAI_API_KEY


class TutorAIService:

    @staticmethod
    def generate_tutor_response(session, user_message, include_context=True, request_explanation=False,
                                request_examples=False):
        """Generate AI tutor response based on user message and context"""
        try:
            # Build conversation context
            context_messages = []

            if include_context:
                recent_messages = session.messages.order_by('-timestamp')[:10]
                for msg in reversed(recent_messages):
                    role = "user" if msg.message_type == "user" else "assistant"
                    context_messages.append({
                        "role": role,
                        "content": msg.content
                    })

            # Build system prompt based on session type and preferences
            system_prompt = TutorAIService._build_system_prompt(
                session, request_explanation, request_examples
            )

            # Prepare messages for API
            messages = [
                           {"role": "system", "content": system_prompt}
                       ] + context_messages + [
                           {"role": "user", "content": user_message}
                       ]

            # Generate response
            start_time = timezone.now()
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )

            end_time = timezone.now()
            response_time = int((end_time - start_time).total_seconds() * 1000)

            tutor_response = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            # Analyze the response for insights
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
                tokens_used=tokens_used,
                response_time_ms=response_time
            )

            # Update session activity
            session.last_activity = timezone.now()
            session.save()

            return {
                'response': tutor_response,
                'message_id': tutor_msg.id,
                'tokens_used': tokens_used,
                'response_time_ms': response_time,
                'intent': intent,
                'topics': topics
            }

        except Exception as e:
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
    def _build_system_prompt(session, request_explanation=False, request_examples=False):
        """Build system prompt based on session context"""
        base_prompt = f"""You are an AI tutor specialized in {session.subject or 'general education'}. 
        You are helping a {session.difficulty_level} level student.

        Your role is to:
        1. Provide clear, helpful explanations
        2. Ask guiding questions to promote learning
        3. Be encouraging and supportive
        4. Adapt to the student's learning pace
        5. Provide step-by-step guidance when needed

        Session type: {session.get_session_type_display()}
        """

        if session.session_type == 'problem_solving':
            base_prompt += """
            Focus on:
            - Breaking down problems into manageable steps
            - Teaching problem-solving strategies
            - Providing hints rather than direct answers initially
            - Encouraging critical thinking
            """

        elif session.session_type == 'concept_explanation':
            base_prompt += """
            Focus on:
            - Clear, simple explanations
            - Using analogies and real-world examples
            - Building from basic to complex concepts
            - Checking understanding frequently
            """

        if request_explanation:
            base_prompt += "\nThe student is specifically requesting a detailed explanation."

        if request_examples:
            base_prompt += "\nThe student is requesting examples to illustrate the concept."

        base_prompt += "\n\nAlways be concise but thorough, and maintain an encouraging tone."

        return base_prompt

    @staticmethod
    def _analyze_message_content(message):
        """Analyze user message to extract intent, confidence, and topics"""
        try:
            prompt = f"""
            Analyze this student message for:
            1. Intent (question, explanation_request, problem_help, clarification, etc.)
            2. Confidence level (0.0-1.0)
            3. Key topics mentioned

            Message: "{message}"

            Respond with JSON:
            {{
                "intent": "...",
                "confidence": 0.0-1.0,
                "topics": ["topic1", "topic2"]
            }}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a message analyzer. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )

            analysis = json.loads(response.choices[0].message.content)
            return analysis.get('intent', 'general'), analysis.get('confidence', 0.5), analysis.get('topics', [])

        except:
            # Fallback analysis
            return 'general', 0.5, []

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

            prompt = f"""
            Solve this {problem_type} problem at {difficulty} level:

            Problem: {problem}

            Provide a comprehensive solution with:
            1. Problem analysis
            2. Step-by-step solution
            3. Final answer
            4. Key concepts used
            5. Similar problems for practice
            6. Learning resources

            Format as JSON:
            {{
                "analysis": "...",
                "solution_steps": [
                    {{"step": 1, "description": "...", "work": "..."}},
                    {{"step": 2, "description": "...", "work": "..."}}
                ],
                "final_answer": "...",
                "explanation": "...",
                "key_concepts": ["concept1", "concept2"],
                "similar_problems": [
                    {{"problem": "...", "difficulty": "easy|medium|hard"}},
                    {{"problem": "...", "difficulty": "easy|medium|hard"}}
                ],
                "learning_resources": [
                    {{"title": "...", "type": "video|article|tutorial", "url": "..."}}
                ]
            }}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": f"You are an expert {problem_type} tutor. Provide detailed, educational solutions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            solution_data = json.loads(response.choices[0].message.content)

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
            # Fallback solution
            return {
                'analysis': f'This is a {problem_type} problem that requires systematic approach.',
                'solution_steps': [
                    {'step': 1, 'description': 'Analyze the problem', 'work': 'Identify known and unknown variables'},
                    {'step': 2, 'description': 'Apply relevant concepts',
                     'work': 'Use appropriate formulas or methods'},
                    {'step': 3, 'description': 'Calculate result', 'work': 'Perform calculations step by step'}
                ],
                'final_answer': 'Please provide more specific problem details for accurate solution',
                'explanation': 'A systematic approach helps solve problems effectively.',
                'key_concepts': [problem_type, 'problem-solving'],
                'similar_problems': [],
                'learning_resources': []
            }

    @staticmethod
    def explain_concept(concept_explanation):
        """Generate comprehensive concept explanation"""
        try:
            concept = concept_explanation.concept_name
            subject = concept_explanation.subject_area
            request = concept_explanation.explanation_request

            prompt = f"""
            Provide a comprehensive explanation of the concept: "{concept}" in {subject}.

            Student's specific request: {request}

            Include:
            1. Clear definition and explanation
            2. Real-world examples (at least 3)
            3. Helpful analogies
            4. Prerequisites to understand this concept
            5. Related concepts to explore
            6. Practice questions
            7. Visual aid suggestions

            Format as JSON:
            {{
                "explanation": "...",
                "examples": [
                    {{"title": "...", "description": "...", "context": "..."}},
                    {{"title": "...", "description": "...", "context": "..."}}
                ],
                "analogies": [
                    {{"analogy": "...", "explanation": "..."}},
                    {{"analogy": "...", "explanation": "..."}}
                ],
                "prerequisites": ["prereq1", "prereq2"],
                "related_concepts": ["concept1", "concept2"],
                "practice_questions": [
                    {{"question": "...", "difficulty": "easy|medium|hard"}},
                    {{"question": "...", "difficulty": "easy|medium|hard"}}
                ],
                "visual_aids": [
                    {{"type": "diagram", "description": "...", "suggestion": "..."}},
                    {{"type": "chart", "description": "...", "suggestion": "..."}}
                ]
            }}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": f"You are an expert {subject} educator. Provide clear, comprehensive explanations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.8
            )

            explanation_data = json.loads(response.choices[0].message.content)

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
            # Fallback explanation
            fallback_data = {
                'explanation': f'{concept} is an important concept in {subject} that requires understanding of fundamental principles.',
                'examples': [
                    {'title': 'Basic Example', 'description': f'A simple example of {concept}',
                     'context': 'everyday situation'},
                    {'title': 'Advanced Example', 'description': f'A more complex application of {concept}',
                     'context': 'professional context'}
                ],
                'analogies': [
                    {'analogy': f'{concept} is like...', 'explanation': 'This analogy helps understand the concept'}],
                'prerequisites': ['basic foundation knowledge'],
                'related_concepts': [f'concepts related to {concept}'],
                'practice_questions': [
                    {'question': f'What is the main principle behind {concept}?', 'difficulty': 'easy'},
                    {'question': f'How would you apply {concept} in real situations?', 'difficulty': 'medium'}
                ],
                'visual_aids': [{'type': 'diagram', 'description': f'Visual representation of {concept}',
                                 'suggestion': 'Create a simple diagram'}]
            }

            # Update with fallback
            concept_explanation.explanation = fallback_data['explanation']
            concept_explanation.examples = fallback_data['examples']
            concept_explanation.analogies = fallback_data['analogies']
            concept_explanation.save()

            return fallback_data

    @staticmethod
    def generate_study_plan(plan_data):
        """Generate AI-powered personalized study plan"""
        try:
            prompt = f"""
            Create a comprehensive study plan:

            Subject: {plan_data['subject']}
            Topics: {', '.join(plan_data['topics'])}
            Duration: {plan_data['duration_days']} days
            Daily study time: {plan_data['daily_study_time']} minutes
            Difficulty level: {plan_data['difficulty_level']}
            Learning style: {plan_data['learning_style']}
            Goals: {', '.join(plan_data.get('goals', []))}

            Create a detailed study schedule with:
            1. Daily tasks and topics
            2. Milestones and checkpoints
            3. Recommended resources
            4. Progress tracking methods

            Format as JSON:
            {{
                "study_schedule": {{
                    "day_1": {{
                        "topics": ["topic1", "topic2"],
                        "tasks": [
                            {{"task": "...", "duration_minutes": 30, "type": "reading|practice|review"}},
                            {{"task": "...", "duration_minutes": 30, "type": "reading|practice|review"}}
                        ],
                        "goals": ["goal1", "goal2"]
                    }},
                    "day_2": {{...}}
                }},
                "milestones": [
                    {{"day": 3, "milestone": "...", "assessment": "..."}},
                    {{"day": 7, "milestone": "...", "assessment": "..."}}
                ],
                "resources": [
                    {{"title": "...", "type": "book|video|website", "url": "...", "topics": ["topic1"]}},
                    {{"title": "...", "type": "book|video|website", "url": "...", "topics": ["topic2"]}}
                ],
                "total_tasks": number,
                "study_tips": ["tip1", "tip2", "tip3"]
            }}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an expert study planner. Create detailed, realistic study schedules."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.7
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            # Fallback study plan
            duration = plan_data['duration_days']
            daily_time = plan_data['daily_study_time']
            topics = plan_data['topics']

            # Create basic schedule
            schedule = {}
            topics_per_day = max(1, len(topics) // duration)

            for day in range(1, duration + 1):
                day_topics = topics[:topics_per_day]
                topics = topics[topics_per_day:]

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
                "study_tips": ["Study consistently", "Take breaks", "Review regularly"]
            }

    @staticmethod
    def generate_learning_insights(user):
        """Generate personalized learning insights based on user activity"""
        try:
            # Collect user data
            sessions = TutorSession.objects.filter(user=user).order_by('-started_at')[:20]
            messages = ChatMessage.objects.filter(session__user=user).order_by('-timestamp')[:50]

            # Analyze patterns
            session_data = []
            for session in sessions:
                session_data.append({
                    'type': session.session_type,
                    'subject': session.subject,
                    'duration': session.duration_minutes,
                    'rating': session.user_rating,
                    'message_count': session.messages.count()
                })

            # Generate insights
            insights = []

            # Study frequency insight
            if sessions.count() >= 5:
                avg_gap = TutorAIService._calculate_average_session_gap(sessions)
                if avg_gap > 7:
                    insights.append({
                        'type': 'pattern',
                        'title': 'Study Frequency Pattern',
                        'description': f'You typically have {avg_gap} days between study sessions. More frequent sessions could improve retention.',
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
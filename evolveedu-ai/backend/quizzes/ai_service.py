# quizzes/ai_service.py
import openai
import json
import random
from django.conf import settings
from .models import Quiz, Question, QuizAttempt, QuizRecommendation

openai.api_key = settings.OPENAI_API_KEY


class QuizAIService:

    @staticmethod
    def generate_quiz_questions(topic, difficulty, question_count, question_types):
        """Generate quiz questions using OpenAI"""
        try:
            question_types_str = ", ".join(question_types)

            prompt = f"""
            Generate {question_count} quiz questions about "{topic}" at {difficulty} level.
            Use these question types: {question_types_str}

            For multiple choice questions:
            - Provide 4 options (A, B, C, D)
            - Only one correct answer
            - Make distractors plausible

            For true/false questions:
            - Clear statement that is definitively true or false

            For short answer questions:
            - Questions that require 1-3 word answers

            Format as JSON array:
            [
                {{
                    "question_text": "...",
                    "question_type": "multiple_choice",
                    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
                    "correct_answers": [0],
                    "explanation": "...",
                    "hint": "...",
                    "points": 1,
                    "difficulty_level": "{difficulty}"
                }},
                {{
                    "question_text": "...",
                    "question_type": "true_false",
                    "options": ["True", "False"],
                    "correct_answers": [0],
                    "explanation": "...",
                    "hint": "...",
                    "points": 1,
                    "difficulty_level": "{difficulty}"
                }}
            ]

            Ensure variety in question difficulty and comprehensive topic coverage.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an expert quiz creator. Generate educational quiz questions in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.7
            )

            questions_data = json.loads(response.choices[0].message.content)
            return questions_data

        except Exception as e:
            # Fallback questions if AI fails
            return QuizAIService._generate_fallback_questions(topic, question_count, difficulty)

    @staticmethod
    def _generate_fallback_questions(topic, question_count, difficulty):
        """Generate fallback questions when AI service fails"""
        fallback_questions = []

        for i in range(min(question_count, 5)):  # Limit fallback questions
            question = {
                "question_text": f"Question {i + 1}: What is an important concept related to {topic}?",
                "question_type": "multiple_choice",
                "options": [
                    f"A) Concept A about {topic}",
                    f"B) Concept B about {topic}",
                    f"C) Concept C about {topic}",
                    f"D) Concept D about {topic}"
                ],
                "correct_answers": [0],
                "explanation": f"This question tests understanding of {topic} concepts.",
                "hint": f"Think about the fundamental principles of {topic}.",
                "points": 1,
                "difficulty_level": difficulty
            }
            fallback_questions.append(question)

        return fallback_questions

    @staticmethod
    def create_quiz_from_ai(user, topic, difficulty, question_count, question_types, category=None, time_limit=None):
        """Create a complete quiz using AI-generated questions"""

        # Generate questions
        questions_data = QuizAIService.generate_quiz_questions(
            topic, difficulty, question_count, question_types
        )

        # Create quiz
        quiz = Quiz.objects.create(
            title=f"AI Generated Quiz: {topic}",
            description=f"An AI-generated {difficulty} level quiz covering {topic}",
            category=category,
            created_by=user,
            difficulty_level=difficulty,
            quiz_type='practice',
            time_limit_minutes=time_limit,
            total_questions=len(questions_data),
            tags=[topic.lower(), 'ai-generated', difficulty]
        )

        # Create questions
        for i, question_data in enumerate(questions_data):
            Question.objects.create(
                quiz=quiz,
                question_text=question_data['question_text'],
                question_type=question_data['question_type'],
                options=question_data.get('options', []),
                correct_answers=question_data.get('correct_answers', []),
                explanation=question_data.get('explanation', ''),
                hint=question_data.get('hint', ''),
                points=question_data.get('points', 1),
                difficulty_level=question_data.get('difficulty_level', difficulty),
                order=i + 1
            )

        return quiz

    @staticmethod
    def evaluate_quiz_attempt(attempt):
        """Evaluate quiz attempt and provide detailed feedback"""
        try:
            responses = attempt.responses.all()
            total_questions = responses.count()
            correct_count = 0
            total_points = 0
            earned_points = 0

            detailed_feedback = []

            for response in responses:
                question = response.question
                is_correct = False
                points = 0

                # Evaluate based on question type
                if question.question_type == 'multiple_choice':
                    if response.selected_options == question.correct_answers:
                        is_correct = True
                        points = question.points
                        correct_count += 1

                elif question.question_type == 'true_false':
                    if response.selected_options == question.correct_answers:
                        is_correct = True
                        points = question.points
                        correct_count += 1

                elif question.question_type == 'short_answer':
                    # Use AI to evaluate short answers
                    is_correct = QuizAIService._evaluate_short_answer(
                        response.text_answer,
                        question.correct_answers
                    )
                    if is_correct:
                        points = question.points
                        correct_count += 1

                # Update response
                response.is_correct = is_correct
                response.points_earned = points
                response.save()

                total_points += question.points
                earned_points += points

                # Add to feedback
                feedback_item = {
                    'question': question.question_text,
                    'correct': is_correct,
                    'explanation': question.explanation,
                    'user_answer': response.text_answer or response.selected_options,
                    'correct_answer': question.correct_answers
                }
                detailed_feedback.append(feedback_item)

            # Calculate score
            score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0
            passed = score_percentage >= attempt.quiz.passing_score

            # Update attempt
            attempt.total_questions = total_questions
            attempt.correct_answers = correct_count
            attempt.score_percentage = score_percentage
            attempt.total_points = total_points
            attempt.earned_points = earned_points
            attempt.passed = passed
            attempt.status = 'completed'

            # Generate personalized feedback
            feedback_text = QuizAIService._generate_personalized_feedback(
                attempt.quiz.title,
                score_percentage,
                detailed_feedback
            )
            attempt.feedback = feedback_text
            attempt.save()

            # Update quiz stats
            attempt.quiz.update_stats()

            # Update user stats
            user = attempt.user
            user.total_quizzes_taken += 1
            user.save(update_fields=['total_quizzes_taken'])

            return {
                'score_percentage': score_percentage,
                'passed': passed,
                'correct_answers': correct_count,
                'total_questions': total_questions,
                'feedback': feedback_text,
                'detailed_feedback': detailed_feedback
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def _evaluate_short_answer(user_answer, correct_answers):
        """Use AI to evaluate short answer questions"""
        try:
            prompt = f"""
            Evaluate if the user's answer is correct for a short answer question.

            User Answer: "{user_answer}"
            Acceptable Answers: {correct_answers}

            Consider synonyms, different phrasings, and partial credit.
            Respond with only "true" or "false".
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an AI grader. Evaluate answers fairly and respond with only 'true' or 'false'."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )

            result = response.choices[0].message.content.strip().lower()
            return result == "true"

        except:
            # Fallback to simple string matching
            user_answer_lower = user_answer.lower().strip()
            for correct in correct_answers:
                if user_answer_lower == str(correct).lower().strip():
                    return True
            return False

    @staticmethod
    def _generate_personalized_feedback(quiz_title, score, detailed_feedback):
        """Generate personalized feedback based on quiz performance"""
        try:
            correct_count = sum(1 for item in detailed_feedback if item['correct'])
            total_count = len(detailed_feedback)

            prompt = f"""
            Generate personalized feedback for a student who scored {score}% on "{quiz_title}".
            They got {correct_count} out of {total_count} questions correct.

            Provide:
            1. Encouraging opening statement
            2. Areas of strength (if any)
            3. Areas for improvement
            4. Specific study recommendations
            5. Motivational closing

            Keep it concise but helpful (max 200 words).
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a supportive AI tutor providing personalized feedback."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )

            return response.choices[0].message.content

        except:
            # Fallback feedback
            if score >= 80:
                return f"Excellent work! You scored {score}% on {quiz_title}. Keep up the great studying!"
            elif score >= 60:
                return f"Good job! You scored {score}% on {quiz_title}. Review the areas you missed and try again."
            else:
                return f"You scored {score}% on {quiz_title}. Don't worry - this is a learning opportunity. Review the material and practice more."

    @staticmethod
    def generate_recommendations_for_user(user):
        """Generate quiz recommendations based on user's history and preferences"""
        try:
            # Get user's quiz history
            recent_attempts = QuizAttempt.objects.filter(
                user=user,
                status='completed'
            ).order_by('-completed_at')[:10]

            # Analyze performance patterns
            weak_areas = []
            strong_areas = []

            for attempt in recent_attempts:
                if attempt.score_percentage < 70:
                    weak_areas.extend(attempt.quiz.tags)
                elif attempt.score_percentage >= 85:
                    strong_areas.extend(attempt.quiz.tags)

            # Generate recommendations
            recommendations = []

            # Recommend practice quizzes for weak areas
            for area in set(weak_areas):
                quizzes = Quiz.objects.filter(
                    tags__contains=area,
                    is_public=True,
                    difficulty_level='beginner'
                ).exclude(
                    attempts__user=user
                )[:2]

                for quiz in quizzes:
                    recommendation, created = QuizRecommendation.objects.get_or_create(
                        user=user,
                        quiz=quiz,
                        defaults={
                            'reason': f"Practice this topic to improve your understanding of {area}",
                            'confidence_score': 0.8
                        }
                    )
                    if created:
                        recommendations.append(recommendation)

            return recommendations

        except Exception as e:
            return []
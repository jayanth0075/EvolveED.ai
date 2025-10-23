# quizzes/ai_service.py
import requests
import json
import random
import time
import re
from django.conf import settings
from .models import Quiz, Question, QuizAttempt, QuizRecommendation


class QuizAIService:

    @staticmethod
    def call_huggingface_api(prompt, max_retries=3, delay=1):
        """Make API call to Hugging Face with retry logic"""
        headers = {
            "Authorization": f"Bearer {getattr(settings, 'HUGGINGFACE_API_KEY', '')}",
            "Content-Type": "application/json"
        }

        # Using a more suitable model for text generation
        api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 800,
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
                    # Model is loading, wait and retry
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
    def generate_quiz_questions(topic, difficulty, question_count, question_types):
        """Generate quiz questions using Hugging Face"""
        try:
            question_types_str = ", ".join(question_types)

            prompt = f"""Create {question_count} quiz questions about "{topic}" at {difficulty} level.
Include these question types: {question_types_str}

For each question provide:
- Question text
- Question type (multiple_choice, true_false, or short_answer)
- For multiple choice: 4 options with one correct answer
- For true/false: statement that is definitively true or false
- Explanation of the correct answer
- A helpful hint
- Difficulty level

Make questions educational and comprehensive about {topic}."""

            ai_response = QuizAIService.call_huggingface_api(prompt)

            if ai_response:
                # Parse the AI response into structured questions
                questions_data = QuizAIService._parse_questions_from_response(
                    ai_response, topic, difficulty, question_count, question_types
                )
                return questions_data
            else:
                raise Exception("Failed to get response from Hugging Face API")

        except Exception as e:
            print(f"Question generation failed: {str(e)}")
            return QuizAIService._generate_fallback_questions(topic, question_count, difficulty)

    @staticmethod
    def _parse_questions_from_response(ai_response, topic, difficulty, question_count, question_types):
        """Parse AI response and structure it into quiz questions format"""
        questions_data = []

        # Split response into potential questions
        lines = ai_response.split('\n')
        current_question = None

        try:
            question_num = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Look for question patterns
                if (line.endswith('?') or 'question' in line.lower()) and len(line) > 20:
                    if current_question and question_num < question_count:
                        questions_data.append(current_question)

                    question_num += 1
                    if question_num > question_count:
                        break

                    # Determine question type
                    q_type = QuizAIService._determine_question_type(line, question_types)

                    current_question = {
                        "question_text": line,
                        "question_type": q_type,
                        "options": [],
                        "correct_answers": [0],
                        "explanation": f"This question tests understanding of {topic}.",
                        "hint": f"Consider the key concepts of {topic}.",
                        "points": 1,
                        "difficulty_level": difficulty
                    }

                    # Generate options based on question type
                    if q_type == "multiple_choice":
                        current_question["options"] = QuizAIService._generate_mc_options(line, topic)
                    elif q_type == "true_false":
                        current_question["options"] = ["True", "False"]
                        current_question["correct_answers"] = [0 if 'true' in line.lower() else 1]

            # Add the last question
            if current_question and len(questions_data) < question_count:
                questions_data.append(current_question)

        except Exception as e:
            print(f"Parsing error: {str(e)}")

        # Fill remaining questions if needed
        while len(questions_data) < question_count:
            questions_data.extend(QuizAIService._generate_fallback_questions(topic, 1, difficulty))

        return questions_data[:question_count]

    @staticmethod
    def _determine_question_type(question_text, question_types):
        """Determine the most appropriate question type"""
        question_lower = question_text.lower()

        if "true_false" in question_types and (
                'true or false' in question_lower or
                'is it true' in question_lower or
                'correct or incorrect' in question_lower
        ):
            return "true_false"
        elif "short_answer" in question_types and (
                'what is' in question_lower or
                'define' in question_lower or
                'name' in question_lower
        ):
            return "short_answer"
        else:
            return "multiple_choice"

    @staticmethod
    def _generate_mc_options(question_text, topic):
        """Generate multiple choice options for a question"""
        # Simple option generation based on question context
        options = [
            f"A) Primary concept of {topic}",
            f"B) Secondary aspect of {topic}",
            f"C) Related but different concept",
            f"D) Unrelated option"
        ]
        return options

    @staticmethod
    def _generate_fallback_questions(topic, question_count, difficulty):
        """Generate fallback questions when AI service fails"""
        fallback_questions = []

        question_templates = [
            {
                "text": f"What is the main principle behind {topic}?",
                "type": "multiple_choice",
                "options": [
                    f"A) Core concept of {topic}",
                    f"B) Basic principle of {topic}",
                    f"C) Advanced theory of {topic}",
                    f"D) Unrelated concept"
                ]
            },
            {
                "text": f"Which statement about {topic} is correct?",
                "type": "multiple_choice",
                "options": [
                    f"A) {topic} involves specific processes",
                    f"B) {topic} is completely theoretical",
                    f"C) {topic} has no practical applications",
                    f"D) {topic} is outdated"
                ]
            },
            {
                "text": f"{topic} is essential for understanding the subject.",
                "type": "true_false",
                "options": ["True", "False"]
            }
        ]

        for i in range(min(question_count, len(question_templates))):
            template = question_templates[i % len(question_templates)]

            question = {
                "question_text": template["text"],
                "question_type": template["type"],
                "options": template["options"],
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
            prompt = f"""Evaluate if this answer is correct:

User Answer: "{user_answer}"
Correct Answers: {correct_answers}

Consider synonyms and different ways to express the same concept. 
Answer only 'correct' or 'incorrect'."""

            ai_response = QuizAIService.call_huggingface_api(prompt)

            if ai_response and 'correct' in ai_response.lower():
                return 'incorrect' not in ai_response.lower()

            # Fallback to string matching
            user_answer_lower = user_answer.lower().strip()
            for correct in correct_answers:
                if user_answer_lower == str(correct).lower().strip():
                    return True
            return False

        except Exception as e:
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

            prompt = f"""Create encouraging feedback for a student:

Quiz: "{quiz_title}"
Score: {score}% ({correct_count}/{total_count} correct)

Provide personalized feedback including:
1. Encouraging opening
2. Performance assessment
3. Areas for improvement
4. Study recommendations
5. Motivational closing

Keep response under 150 words and be supportive."""

            ai_response = QuizAIService.call_huggingface_api(prompt)

            if ai_response and len(ai_response) > 20:
                return ai_response
            else:
                return QuizAIService._get_fallback_feedback(score, quiz_title)

        except Exception as e:
            return QuizAIService._get_fallback_feedback(score, quiz_title)

    @staticmethod
    def _get_fallback_feedback(score, quiz_title):
        """Generate fallback feedback"""
        if score >= 80:
            return f"Excellent work! You scored {score}% on {quiz_title}. Your understanding of the material is strong. Keep up the great studying!"
        elif score >= 60:
            return f"Good job! You scored {score}% on {quiz_title}. You have a solid foundation. Review the areas you missed and try again to improve further."
        else:
            return f"You scored {score}% on {quiz_title}. Don't be discouraged - this is a learning opportunity! Review the material carefully and practice more. Every expert was once a beginner."

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
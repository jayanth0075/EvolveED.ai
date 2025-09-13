# quizzes/views.py
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Avg, Count
from datetime import timedelta
from .models import Quiz, Question, QuizAttempt, QuizResponse, QuizCategory, QuizRecommendation
from .serializers import (
    QuizSerializer, QuizListSerializer, QuizCreateSerializer, QuestionSerializer,
    QuizAttemptSerializer, QuizAttemptCreateSerializer, QuizResponseSerializer,
    QuizCategorySerializer, QuizRecommendationSerializer, GenerateQuizRequestSerializer,
    QuizSubmissionSerializer
)
from .ai_service import QuizAIService


class QuizCategoryListView(generics.ListCreateAPIView):
    queryset = QuizCategory.objects.all()
    serializer_class = QuizCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class QuizListView(generics.ListAPIView):
    serializer_class = QuizListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Quiz.objects.filter(
            Q(created_by=self.request.user) | Q(is_public=True)
        ).select_related('category', 'created_by')

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        # Filter by quiz type
        quiz_type = self.request.query_params.get('type')
        if quiz_type:
            queryset = queryset.filter(quiz_type=quiz_type)

        # Search in title and description
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Filter by tags
        tags = self.request.query_params.get('tags')
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                queryset = queryset.filter(tags__contains=tag.strip())

        # Sort options
        sort_by = self.request.query_params.get('sort', 'created_at')
        if sort_by == 'popular':
            queryset = queryset.order_by('-times_taken', '-average_score')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'difficulty':
            queryset = queryset.order_by('difficulty_level', 'title')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(
            Q(created_by=self.request.user) | Q(is_public=True)
        ).prefetch_related('questions')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_questions'] = self.request.query_params.get('include_questions', 'true') == 'true'
        return context


class QuizCreateView(generics.CreateAPIView):
    serializer_class = QuizCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_quiz_with_ai(request):
    serializer = GenerateQuizRequestSerializer(data=request.data)
    if serializer.is_valid():
        try:
            topic = serializer.validated_data['topic']
            difficulty = serializer.validated_data['difficulty']
            question_count = serializer.validated_data['question_count']
            question_types = serializer.validated_data['question_types']
            category_id = serializer.validated_data.get('category_id')
            time_limit = serializer.validated_data.get('time_limit')

            category = None
            if category_id:
                category = get_object_or_404(QuizCategory, id=category_id)

            quiz = QuizAIService.create_quiz_from_ai(
                user=request.user,
                topic=topic,
                difficulty=difficulty,
                question_count=question_count,
                question_types=question_types,
                category=category,
                time_limit=time_limit
            )

            return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Check if quiz is accessible
    if not quiz.is_public and quiz.created_by != request.user:
        return Response({'error': 'Quiz not accessible'}, status=status.HTTP_403_FORBIDDEN)

    # Check max attempts
    user_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).count()
    if user_attempts >= quiz.max_attempts:
        return Response({'error': 'Maximum attempts exceeded'}, status=status.HTTP_400_BAD_REQUEST)

    # Create new attempt
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        total_questions=quiz.questions.count()
    )

    # Return quiz questions (without correct answers)
    questions_data = []
    for question in quiz.questions.all():
        question_data = {
            'id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'options': question.options,
            'hint': question.hint if request.query_params.get('show_hints') == 'true' else '',
            'points': question.points,
            'order': question.order,
            'image': question.image.url if question.image else None
        }
        questions_data.append(question_data)

    return Response({
        'attempt_id': attempt.id,
        'quiz': {
            'id': quiz.id,
            'title': quiz.title,
            'description': quiz.description,
            'time_limit_minutes': quiz.time_limit_minutes,
            'total_questions': quiz.total_questions,
            'shuffle_questions': quiz.shuffle_questions
        },
        'questions': questions_data,
        'started_at': attempt.started_at
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_quiz_response(request, attempt_id, question_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user, status='in_progress')
    question = get_object_or_404(Question, id=question_id, quiz=attempt.quiz)

    # Create or update response
    response_data = {
        'selected_options': request.data.get('selected_options', []),
        'text_answer': request.data.get('text_answer', ''),
        'time_spent_seconds': request.data.get('time_spent_seconds', 0)
    }

    response, created = QuizResponse.objects.get_or_create(
        attempt=attempt,
        question=question,
        defaults=response_data
    )

    if not created:
        # Update existing response
        for key, value in response_data.items():
            setattr(response, key, value)
        response.save()

    return Response({'message': 'Response saved successfully'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_quiz_attempt(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user, status='in_progress')

    # Calculate time taken
    time_taken = timezone.now() - attempt.started_at
    attempt.time_taken_minutes = int(time_taken.total_seconds() / 60)
    attempt.completed_at = timezone.now()

    # Evaluate the attempt using AI
    evaluation_result = QuizAIService.evaluate_quiz_attempt(attempt)

    if 'error' in evaluation_result:
        return Response(evaluation_result, status=status.HTTP_400_BAD_REQUEST)

    # Generate new recommendations
    QuizAIService.generate_recommendations_for_user(request.user)

    return Response({
        'attempt_id': attempt.id,
        'quiz_title': attempt.quiz.title,
        'score_percentage': evaluation_result['score_percentage'],
        'passed': evaluation_result['passed'],
        'correct_answers': evaluation_result['correct_answers'],
        'total_questions': evaluation_result['total_questions'],
        'time_taken_minutes': attempt.time_taken_minutes,
        'feedback': evaluation_result['feedback'],
        'show_results_immediately': attempt.quiz.show_results_immediately
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def quiz_attempt_results(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)

    if attempt.status != 'completed':
        return Response({'error': 'Quiz not completed yet'}, status=status.HTTP_400_BAD_REQUEST)

    # Get detailed results
    responses = attempt.responses.all().select_related('question')
    detailed_results = []

    for response in responses:
        question = response.question
        result_data = {
            'question_id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'user_answer': response.text_answer or response.selected_options,
            'correct_answers': question.correct_answers,
            'is_correct': response.is_correct,
            'points_earned': response.points_earned,
            'max_points': question.points,
            'explanation': question.explanation,
            'options': question.options if question.question_type in ['multiple_choice', 'true_false'] else []
        }
        detailed_results.append(result_data)

    return Response({
        'attempt': QuizAttemptSerializer(attempt).data,
        'detailed_results': detailed_results,
        'overall_feedback': attempt.feedback
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_quiz_attempts(request):
    attempts = QuizAttempt.objects.filter(user=request.user).select_related('quiz').order_by('-started_at')

    # Filter by status
    status_filter = request.query_params.get('status')
    if status_filter:
        attempts = attempts.filter(status=status_filter)

    # Filter by quiz
    quiz_id = request.query_params.get('quiz')
    if quiz_id:
        attempts = attempts.filter(quiz_id=quiz_id)

    serializer = QuizAttemptSerializer(attempts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def quiz_recommendations(request):
    recommendations = QuizRecommendation.objects.filter(
        user=request.user,
        is_dismissed=False,
        is_taken=False
    ).select_related('quiz').order_by('-confidence_score', '-created_at')

    serializer = QuizRecommendationSerializer(recommendations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def dismiss_recommendation(request, recommendation_id):
    recommendation = get_object_or_404(
        QuizRecommendation,
        id=recommendation_id,
        user=request.user
    )
    recommendation.is_dismissed = True
    recommendation.save()

    return Response({'message': 'Recommendation dismissed'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def quiz_analytics(request):
    user = request.user

    # Get user's quiz statistics
    attempts = QuizAttempt.objects.filter(user=user, status='completed')

    total_attempts = attempts.count()
    if total_attempts == 0:
        return Response({
            'total_attempts': 0,
            'average_score': 0,
            'success_rate': 0,
            'study_time_hours': 0,
            'favorite_categories': [],
            'performance_trend': []
        })

    average_score = attempts.aggregate(avg_score=Avg('score_percentage'))['avg_score'] or 0
    passed_attempts = attempts.filter(passed=True).count()
    success_rate = (passed_attempts / total_attempts) * 100 if total_attempts > 0 else 0

    total_study_time = attempts.aggregate(total_time=models.Sum('time_taken_minutes'))['total_time'] or 0
    study_time_hours = total_study_time / 60

    # Favorite categories
    category_stats = (attempts
                      .values('quiz__category__name')
                      .annotate(count=Count('id'))
                      .order_by('-count')[:5])

    # Performance trend (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_attempts = (attempts
                       .filter(completed_at__gte=thirty_days_ago)
                       .order_by('completed_at'))

    trend_data = []
    for attempt in recent_attempts:
        trend_data.append({
            'date': attempt.completed_at.date(),
            'score': attempt.score_percentage
        })

    return Response({
        'total_attempts': total_attempts,
        'average_score': round(average_score, 1),
        'success_rate': round(success_rate, 1),
        'study_time_hours': round(study_time_hours, 1),
        'favorite_categories': list(category_stats),
        'performance_trend': trend_data
    })
# quizzes/serializers.py
from rest_framework import serializers
from .models import Quiz, Question, QuizAttempt, QuizResponse, QuizCategory, QuizRecommendation


class QuizCategorySerializer(serializers.ModelSerializer):
    quiz_count = serializers.IntegerField(source='quizzes.count', read_only=True)

    class Meta:
        model = QuizCategory
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['created_at']


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['quiz', 'created_at']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    user_attempts = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'total_questions',
                            'average_score', 'times_taken']

    def get_user_attempts(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.attempts.filter(user=request.user).count()
        return 0


class QuizListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    user_attempts = serializers.SerializerMethodField()
    user_best_score = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'category_name', 'created_by_email',
                  'difficulty_level', 'quiz_type', 'time_limit_minutes', 'total_questions',
                  'average_score', 'times_taken', 'tags', 'user_attempts', 'user_best_score',
                  'created_at']

    def get_user_attempts(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.attempts.filter(user=request.user).count()
        return 0

    def get_user_best_score(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            best_attempt = obj.attempts.filter(user=request.user, status='completed').order_by(
                '-score_percentage').first()
            return best_attempt.score_percentage if best_attempt else None
        return None


class QuizCreateSerializer(serializers.ModelSerializer):
    questions_data = serializers.ListField(child=QuestionCreateSerializer(), write_only=True)

    class Meta:
        model = Quiz
        exclude = ['created_by', 'created_at', 'updated_at', 'total_questions',
                   'average_score', 'times_taken']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions_data', [])
        quiz = Quiz.objects.create(**validated_data)

        for i, question_data in enumerate(questions_data):
            question_data['order'] = i + 1
            Question.objects.create(quiz=quiz, **question_data)

        quiz.total_questions = len(questions_data)
        quiz.save()

        return quiz


class QuizResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResponse
        fields = '__all__'
        read_only_fields = ['attempt', 'is_correct', 'points_earned', 'answered_at']


class QuizAttemptSerializer(serializers.ModelSerializer):
    responses = QuizResponseSerializer(many=True, read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)

    class Meta:
        model = QuizAttempt
        fields = '__all__'
        read_only_fields = ['user', 'started_at', 'completed_at', 'total_questions',
                            'correct_answers', 'score_percentage', 'total_points',
                            'earned_points', 'time_taken_minutes', 'passed']


class QuizAttemptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['quiz']


class QuizSubmissionSerializer(serializers.Serializer):
    responses = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )


class QuizRecommendationSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    quiz_description = serializers.CharField(source='quiz.description', read_only=True)
    quiz_difficulty = serializers.CharField(source='quiz.difficulty_level', read_only=True)
    quiz_category = serializers.CharField(source='quiz.category.name', read_only=True)

    class Meta:
        model = QuizRecommendation
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class GenerateQuizRequestSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=200)
    difficulty = serializers.ChoiceField(choices=Quiz.DIFFICULTY_CHOICES, default='intermediate')
    question_count = serializers.IntegerField(min_value=5, max_value=50, default=10)
    question_types = serializers.ListField(
        child=serializers.ChoiceField(choices=Question.QUESTION_TYPES),
        default=['multiple_choice']
    )
    category_id = serializers.IntegerField(required=False)
    time_limit = serializers.IntegerField(required=False, min_value=1)  # in minutes
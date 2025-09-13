# tutor/serializers.py
from rest_framework import serializers
from .models import (
    TutorSession, ChatMessage, ProblemSolvingSession, ConceptExplanation,
    StudyPlan, LearningInsight, TutorFeedback
)


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = ['session', 'timestamp', 'tokens_used', 'response_time_ms',
                            'intent', 'confidence_score', 'topic_tags']


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['content', 'message_type']


class TutorSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.IntegerField(source='messages.count', read_only=True)

    class Meta:
        model = TutorSession
        fields = '__all__'
        read_only_fields = ['user', 'started_at', 'last_activity', 'completed_at',
                            'duration_minutes', 'session_summary']


class TutorSessionListSerializer(serializers.ModelSerializer):
    message_count = serializers.IntegerField(source='messages.count', read_only=True)
    last_message_time = serializers.SerializerMethodField()

    class Meta:
        model = TutorSession
        fields = ['id', 'title', 'session_type', 'subject', 'status', 'difficulty_level',
                  'started_at', 'last_activity', 'duration_minutes', 'message_count',
                  'user_rating', 'last_message_time']

    def get_last_message_time(self, obj):
        last_message = obj.messages.first()
        return last_message.timestamp if last_message else None


class TutorSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorSession
        fields = ['session_type', 'title', 'subject', 'difficulty_level', 'learning_objectives']


class ProblemSolvingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemSolvingSession
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'solution_steps', 'final_answer',
                            'explanation', 'key_concepts', 'similar_problems',
                            'learning_resources', 'understanding_score']


class ProblemSolvingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemSolvingSession
        fields = ['problem_statement', 'problem_type', 'difficulty_level',
                  'problem_image', 'problem_file']


class ConceptExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptExplanation
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'explanation', 'examples', 'analogies',
                            'visual_aids', 'prerequisites', 'related_concepts', 'practice_questions']


class ConceptExplanationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptExplanation
        fields = ['concept_name', 'subject_area', 'explanation_request']


class StudyPlanSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = StudyPlan
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'study_schedule', 'milestones',
                            'resources', 'total_tasks']

    def get_progress_percentage(self, obj):
        if obj.total_tasks > 0:
            return round((obj.tasks_completed / obj.total_tasks) * 100, 1)
        return 0

    def get_days_remaining(self, obj):
        from django.utils import timezone
        if obj.end_date > timezone.now().date():
            return (obj.end_date - timezone.now().date()).days
        return 0


class StudyPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPlan
        fields = ['title', 'description', 'plan_type', 'subject', 'topics',
                  'duration_days', 'daily_study_time', 'start_date']


class LearningInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningInsight
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'confidence_score', 'supporting_data',
                            'metrics', 'suggested_actions']


class TutorFeedbackSerializer(serializers.ModelSerializer):
    session_title = serializers.CharField(source='session.title', read_only=True)

    class Meta:
        model = TutorFeedback
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'is_resolved', 'admin_response']


class TutorFeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorFeedback
        fields = ['session', 'feedback_type', 'rating', 'title', 'content',
                  'content_quality', 'response_speed', 'helpfulness', 'user_experience']


class StartChatSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    session_type = serializers.ChoiceField(choices=TutorSession.SESSION_TYPES, default='chat')
    subject = serializers.CharField(max_length=100, required=False, default='')
    difficulty_level = serializers.ChoiceField(choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='intermediate')


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    include_context = serializers.BooleanField(default=True)
    request_explanation = serializers.BooleanField(default=False)
    request_examples = serializers.BooleanField(default=False)


class GenerateStudyPlanSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=100)
    topics = serializers.ListField(child=serializers.CharField(), min_length=1)
    duration_days = serializers.IntegerField(min_value=1, max_value=365, default=7)
    daily_study_time = serializers.IntegerField(min_value=15, max_value=480, default=60)  # 15 min to 8 hours
    difficulty_level = serializers.ChoiceField(choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='intermediate')
    learning_style = serializers.ChoiceField(choices=[
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('reading', 'Reading/Writing'),
        ('kinesthetic', 'Hands-on'),
        ('mixed', 'Mixed'),
    ], default='mixed')
    goals = serializers.ListField(child=serializers.CharField(), required=False, default=list)
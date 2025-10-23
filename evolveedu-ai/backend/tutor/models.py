# tutor/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TutorSession(models.Model):
    """Model to track AI tutor sessions and interactions."""
    SESSION_TYPES = [
        ('chat', 'Chat Session'),
        ('problem_solving', 'Problem Solving'),
        ('concept_explanation', 'Concept Explanation'),
        ('homework_help', 'Homework Help'),
        ('exam_prep', 'Exam Preparation'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_sessions')
    session_type = models.CharField(max_length=30, choices=SESSION_TYPES, default='chat')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, blank=True)

    # Session metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='intermediate')

    # Tracking
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)

    # AI context
    context_data = models.JSONField(default=dict, blank=True)  # Store conversation context
    learning_objectives = models.JSONField(default=list, blank=True)

    # Feedback and rating
    user_rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    user_feedback = models.TextField(blank=True)
    session_summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.title} ({self.session_type})"

    class Meta:
        ordering = ['-started_at']


class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('tutor', 'AI Tutor Response'),
        ('system', 'System Message'),
    ]

    session = models.ForeignKey(TutorSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()

    # Message metadata
    timestamp = models.DateTimeField(auto_now_add=True)
    tokens_used = models.IntegerField(default=0)
    response_time_ms = models.IntegerField(default=0)

    # Content analysis
    intent = models.CharField(max_length=50, blank=True)  # question, explanation_request, etc.
    confidence_score = models.FloatField(default=0.0)
    topic_tags = models.JSONField(default=list, blank=True)

    # User interaction
    is_helpful = models.BooleanField(null=True, blank=True)  # User feedback on tutor responses
    needs_followup = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.session.title} - {self.message_type} - {self.timestamp}"

    class Meta:
        ordering = ['timestamp']


class ProblemSolvingSession(models.Model):
    PROBLEM_TYPES = [
        ('math', 'Mathematics'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('programming', 'Programming'),
        ('logic', 'Logic/Reasoning'),
        ('general', 'General Problem'),
    ]

    STATUS_CHOICES = [
        ('analyzing', 'Analyzing Problem'),
        ('solving', 'Working on Solution'),
        ('reviewing', 'Reviewing Solution'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_sessions')
    tutor_session = models.OneToOneField(TutorSession, on_delete=models.CASCADE, related_name='problem_session')

    # Problem details
    problem_statement = models.TextField()
    problem_type = models.CharField(max_length=20, choices=PROBLEM_TYPES, default='general')
    difficulty_level = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium')

    # Problem attachments
    problem_image = models.ImageField(upload_to='problem_images/', blank=True, null=True)
    problem_file = models.FileField(upload_to='problem_files/', blank=True, null=True)

    # Solution process
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='analyzing')
    solution_steps = models.JSONField(default=list, blank=True)
    final_answer = models.TextField(blank=True)
    explanation = models.TextField(blank=True)

    # AI analysis
    key_concepts = models.JSONField(default=list, blank=True)
    similar_problems = models.JSONField(default=list, blank=True)
    learning_resources = models.JSONField(default=list, blank=True)

    # User progress
    hints_used = models.IntegerField(default=0)
    attempts_made = models.IntegerField(default=0)
    time_spent_minutes = models.IntegerField(default=0)
    understanding_score = models.IntegerField(default=0)  # 0-100

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Problem: {self.problem_type} - {self.user.email}"


class ConceptExplanation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='concept_explanations')
    tutor_session = models.OneToOneField(TutorSession, on_delete=models.CASCADE, related_name='concept_explanation')

    # Concept details
    concept_name = models.CharField(max_length=200)
    subject_area = models.CharField(max_length=100)
    explanation_request = models.TextField()

    # AI-generated explanation
    explanation = models.TextField()
    examples = models.JSONField(default=list, blank=True)
    analogies = models.JSONField(default=list, blank=True)
    visual_aids = models.JSONField(default=list, blank=True)  # URLs to diagrams, videos, etc.

    # Related content
    prerequisites = models.JSONField(default=list, blank=True)
    related_concepts = models.JSONField(default=list, blank=True)
    practice_questions = models.JSONField(default=list, blank=True)

    # User interaction
    explanation_rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    clarity_score = models.IntegerField(null=True, blank=True)  # 1-100
    follow_up_questions = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Explanation: {self.concept_name} - {self.user.email}"


class StudyPlan(models.Model):
    PLAN_TYPES = [
        ('daily', 'Daily Plan'),
        ('weekly', 'Weekly Plan'),
        ('exam_prep', 'Exam Preparation'),
        ('topic_mastery', 'Topic Mastery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_plans')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default='weekly')

    # Plan details
    subject = models.CharField(max_length=100)
    topics = models.JSONField(default=list)  # List of topics to cover
    duration_days = models.IntegerField(default=7)
    daily_study_time = models.IntegerField(default=60)  # minutes

    # AI-generated plan
    study_schedule = models.JSONField(default=dict)  # {day: {tasks: [], time: int}}
    milestones = models.JSONField(default=list)
    resources = models.JSONField(default=list)

    # Progress tracking
    current_day = models.IntegerField(default=1)
    completion_percentage = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    total_tasks = models.IntegerField(default=0)

    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Effectiveness
    adherence_score = models.IntegerField(default=0)  # 0-100
    effectiveness_rating = models.IntegerField(null=True, blank=True)  # 1-5 stars

    def __str__(self):
        return f"{self.title} - {self.user.email}"


class LearningInsight(models.Model):
    INSIGHT_TYPES = [
        ('strength', 'Learning Strength'),
        ('weakness', 'Area for Improvement'),
        ('pattern', 'Learning Pattern'),
        ('recommendation', 'Study Recommendation'),
        ('achievement', 'Learning Achievement'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_insights')
    insight_type = models.CharField(max_length=20, choices=INSIGHT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Context
    subject_area = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(default=0.0)  # AI confidence in this insight

    # Data supporting the insight
    supporting_data = models.JSONField(default=dict, blank=True)
    metrics = models.JSONField(default=dict, blank=True)

    # Actionability
    is_actionable = models.BooleanField(default=True)
    suggested_actions = models.JSONField(default=list, blank=True)
    priority_level = models.CharField(max_length=10, choices=[
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ], default='medium')

    # User interaction
    is_acknowledged = models.BooleanField(default=False)
    is_helpful = models.BooleanField(null=True, blank=True)
    user_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # Some insights may expire

    def __str__(self):
        return f"{self.insight_type}: {self.title} - {self.user.email}"

    class Meta:
        ordering = ['-created_at']


class TutorFeedback(models.Model):
    FEEDBACK_TYPES = [
        ('session_rating', 'Session Rating'),
        ('feature_request', 'Feature Request'),
        ('bug_report', 'Bug Report'),
        ('general', 'General Feedback'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_feedback')
    session = models.ForeignKey(TutorSession, on_delete=models.SET_NULL, null=True, blank=True)

    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, default='general')
    rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    title = models.CharField(max_length=200)
    content = models.TextField()

    # Specific feedback areas
    content_quality = models.IntegerField(null=True, blank=True)  # 1-5
    response_speed = models.IntegerField(null=True, blank=True)  # 1-5
    helpfulness = models.IntegerField(null=True, blank=True)  # 1-5
    user_experience = models.IntegerField(null=True, blank=True)  # 1-5

    # Follow-up
    is_resolved = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback: {self.feedback_type} - {self.user.email}"
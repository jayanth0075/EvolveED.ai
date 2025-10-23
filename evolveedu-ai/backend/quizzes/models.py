# quizzes/models.py
from django.db import models
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class QuizCategory(models.Model):
    """Model to categorize quizzes by subject."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='🧠')

    def __str__(self):
        """Return the category name."""
        return self.name

    class Meta:
        verbose_name_plural = "Quiz Categories"


class Quiz(models.Model):
    """Model to store quiz information and metadata."""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    QUIZ_TYPE_CHOICES = [
        ('practice', 'Practice Quiz'),
        ('assessment', 'Assessment'),
        ('adaptive', 'Adaptive Quiz'),
        ('timed', 'Timed Quiz'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE, related_name='quizzes')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES, default='practice')

    # Quiz settings
    time_limit_minutes = models.IntegerField(null=True, blank=True)  # None for unlimited
    max_attempts = models.IntegerField(default=3)
    passing_score = models.IntegerField(default=70)  # Percentage
    show_results_immediately = models.BooleanField(default=True)
    shuffle_questions = models.BooleanField(default=True)

    # Metadata
    is_public = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    total_questions = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    times_taken = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def update_stats(self):
        """Update quiz statistics"""
        attempts = self.attempts.all()
        if attempts:
            self.times_taken = attempts.count()
            self.average_score = sum([a.score_percentage for a in attempts]) / attempts.count()
            self.save(update_fields=['times_taken', 'average_score'])


class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
        ('fill_blank', 'Fill in the Blank'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')

    # For multiple choice questions
    options = models.JSONField(default=list, blank=True)  # List of options
    correct_answers = models.JSONField(default=list)  # List of correct answer indices/values

    # Explanation and hints
    explanation = models.TextField(blank=True)
    hint = models.TextField(blank=True)

    # Scoring
    points = models.IntegerField(default=1)
    difficulty_level = models.CharField(max_length=20, choices=Quiz.DIFFICULTY_CHOICES, default='intermediate')

    # Metadata
    order = models.IntegerField(default=0)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"

    class Meta:
        ordering = ['order']


class QuizAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    # Scoring
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    score_percentage = models.FloatField(default=0.0)
    total_points = models.IntegerField(default=0)
    earned_points = models.IntegerField(default=0)

    # Time tracking
    time_taken_minutes = models.IntegerField(default=0)

    # Results
    passed = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.score_percentage}%"

    class Meta:
        ordering = ['-started_at']


class QuizResponse(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # User's answer
    selected_options = models.JSONField(default=list, blank=True)  # For multiple choice
    text_answer = models.TextField(blank=True)  # For text-based questions

    # Scoring
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)

    # Timing
    time_spent_seconds = models.IntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attempt.user.email} - {self.question.quiz.title} - Q{self.question.order}"


class QuizRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_recommendations')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='recommendations')

    # Recommendation details
    reason = models.TextField()  # Why this quiz is recommended
    confidence_score = models.FloatField()  # 0.0 to 1.0

    # User interaction
    is_dismissed = models.BooleanField(default=False)
    is_taken = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommend {self.quiz.title} to {self.user.email}"

    class Meta:
        unique_together = ['user', 'quiz']
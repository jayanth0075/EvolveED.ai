# accounts/models.py
from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('teacher', 'Teacher'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    # Career/Education fields
    current_education = models.CharField(max_length=100, blank=True)
    current_job = models.CharField(max_length=100, blank=True)
    skills = models.JSONField(default=list, blank=True)
    interests = models.JSONField(default=list, blank=True)

    # Progress tracking
    total_quizzes_taken = models.IntegerField(default=0)
    total_notes_generated = models.IntegerField(default=0)
    current_level = models.CharField(max_length=20, default='Beginner')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """Return the email address of the user."""
        return self.email


class UserProgress(models.Model):
    """Model to track user learning progress and achievements."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')
    total_study_time = models.IntegerField(default=0)  # in minutes
    completed_roadmaps = models.JSONField(default=list)
    current_roadmaps = models.JSONField(default=list)
    achievements = models.JSONField(default=list)
    streak_days = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the user progress representation."""
        return f"{self.user.email} - Progress"
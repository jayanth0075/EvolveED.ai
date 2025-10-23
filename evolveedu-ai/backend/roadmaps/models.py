# roadmaps/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SkillCategory(models.Model):
    """Model to categorize skills and learning paths."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='🎯')

    def __str__(self):
        """Return the category name."""
        return self.name

    class Meta:
        verbose_name_plural = "Skill Categories"


class Skill(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')

    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='unlocks')

    # Estimated learning metrics
    estimated_hours = models.IntegerField(default=10)  # Hours to learn
    market_demand = models.IntegerField(default=50)  # 1-100 scale
    avg_salary_impact = models.IntegerField(default=0)  # USD per year

    # Resources
    learning_resources = models.JSONField(default=list, blank=True)  # URLs, books, courses
    practice_projects = models.JSONField(default=list, blank=True)

    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'category']


class CareerPath(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='career_paths')

    # Career details
    average_salary_min = models.IntegerField(default=0)
    average_salary_max = models.IntegerField(default=0)
    job_growth_rate = models.FloatField(default=0.0)  # Percentage

    required_skills = models.ManyToManyField(Skill, related_name='required_for_paths')
    recommended_skills = models.ManyToManyField(Skill, related_name='recommended_for_paths', blank=True)

    # Learning path
    total_estimated_months = models.IntegerField(default=12)
    difficulty_level = models.CharField(max_length=20, choices=Skill.DIFFICULTY_LEVELS, default='intermediate')

    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PersonalizedRoadmap(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roadmaps')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Goal settings
    target_career_path = models.ForeignKey(CareerPath, on_delete=models.SET_NULL, null=True, blank=True)
    target_skills = models.ManyToManyField(Skill, related_name='targeted_by_roadmaps')
    current_skill_level = models.JSONField(default=dict)  # {skill_id: level}

    # Timeline
    start_date = models.DateField()
    target_completion_date = models.DateField()
    estimated_hours_per_week = models.IntegerField(default=10)

    # Progress tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    overall_progress_percentage = models.IntegerField(default=0)
    completed_milestones = models.JSONField(default=list)

    # AI generated content
    personalized_recommendations = models.JSONField(default=list)
    weekly_goals = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.title}"


class RoadmapMilestone(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]

    roadmap = models.ForeignKey(PersonalizedRoadmap, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Associated learning content
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='milestones')
    learning_resources = models.JSONField(default=list)
    practice_tasks = models.JSONField(default=list)

    # Progress tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress_percentage = models.IntegerField(default=0)
    estimated_hours = models.IntegerField(default=5)
    actual_hours_spent = models.IntegerField(default=0)

    # Timeline
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)

    # Ordering
    order = models.IntegerField(default=0)

    # Assessment
    completion_criteria = models.JSONField(default=list)
    assessment_score = models.IntegerField(null=True, blank=True)  # 0-100

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.roadmap.title} - {self.title}"

    class Meta:
        ordering = ['order']


class SkillAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_assessments')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='assessments')

    # Assessment details
    current_level = models.CharField(max_length=20, choices=Skill.DIFFICULTY_LEVELS)
    confidence_score = models.IntegerField()  # 1-100

    # Evidence/proof
    projects_completed = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    years_of_experience = models.FloatField(default=0.0)

    # Assessment method
    assessment_method = models.CharField(max_length=50, default='self_assessment')  # self, quiz, project, etc.
    assessment_date = models.DateTimeField(auto_now_add=True)

    # AI analysis
    skill_gaps = models.JSONField(default=list)
    improvement_suggestions = models.JSONField(default=list)
    next_learning_steps = models.JSONField(default=list)

    def __str__(self):
        return f"{self.user.email} - {self.skill.name} - {self.current_level}"

    class Meta:
        unique_together = ['user', 'skill']


class LearningResource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('course', 'Online Course'),
        ('book', 'Book'),
        ('tutorial', 'Tutorial'),
        ('documentation', 'Documentation'),
        ('project', 'Project'),
        ('practice', 'Practice Exercise'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)

    # Associations
    skills = models.ManyToManyField(Skill, related_name='resources')
    difficulty_level = models.CharField(max_length=20, choices=Skill.DIFFICULTY_LEVELS, default='beginner')

    # Metadata
    estimated_duration = models.CharField(max_length=50, blank=True)  # "2 hours", "3 weeks", etc.
    cost = models.CharField(max_length=20, default='free')  # free, paid, premium
    rating = models.FloatField(default=0.0)
    provider = models.CharField(max_length=100, blank=True)

    # AI analysis
    content_quality_score = models.IntegerField(default=80)  # 0-100
    relevance_score = models.IntegerField(default=80)  # 0-100

    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress')
    resource = models.ForeignKey(LearningResource, on_delete=models.CASCADE, related_name='user_progress')
    roadmap = models.ForeignKey(PersonalizedRoadmap, on_delete=models.CASCADE, null=True, blank=True)

    # Progress tracking
    status = models.CharField(max_length=20, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('bookmarked', 'Bookmarked'),
    ], default='not_started')

    progress_percentage = models.IntegerField(default=0)
    time_spent_minutes = models.IntegerField(default=0)

    # Dates
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    # User feedback
    rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    review = models.TextField(blank=True)
    would_recommend = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.resource.title} - {self.progress_percentage}%"

    class Meta:
        unique_together = ['user', 'resource']
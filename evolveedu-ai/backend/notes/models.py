# notes/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class NoteCategory(models.Model):
    """Model to organize notes into categories."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='📝')

    def __str__(self):
        """Return the category name."""
        return self.name

    class Meta:
        verbose_name_plural = "Note Categories"


class Note(models.Model):
    SOURCE_CHOICES = [
        ('youtube', 'YouTube Video'),
        ('pdf', 'PDF Document'),
        ('text', 'Text Input'),
        ('lecture', 'Lecture Audio'),
        ('url', 'Web URL'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(blank=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    source_url = models.URLField(blank=True, null=True)
    source_file = models.FileField(upload_to='note_sources/', blank=True, null=True)

    category = models.ForeignKey(NoteCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)

    # AI generated fields
    key_points = models.JSONField(default=list, blank=True)
    questions = models.JSONField(default=list, blank=True)
    difficulty_level = models.CharField(max_length=20, default='Medium')
    estimated_read_time = models.IntegerField(default=5)  # in minutes

    # Metadata
    is_public = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_notes', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the note title."""
        return self.title

    class Meta:
        ordering = ['-created_at']


class NoteShare(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shares')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notes')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        """Return share information."""
        return f"{self.shared_by.email} shared {self.note.title} with {self.shared_with.email}"


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    notes = models.ManyToManyField(Note, related_name='study_sessions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.IntegerField(default=0)

    completed = models.BooleanField(default=False)
    notes_reviewed = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return study session information."""
        return f"{self.user.email} - {self.title}"
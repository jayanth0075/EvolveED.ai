# notes/serializers.py
from rest_framework import serializers
from .models import Note, NoteCategory, NoteShare, StudySession


class NoteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteCategory
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['user', 'views', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'source_type', 'source_url', 'source_file', 'category', 'tags', 'is_public']


class NoteShareSerializer(serializers.ModelSerializer):
    shared_by_email = serializers.CharField(source='shared_by.email', read_only=True)
    shared_with_email = serializers.CharField(source='shared_with.email', read_only=True)
    note_title = serializers.CharField(source='note.title', read_only=True)

    class Meta:
        model = NoteShare
        fields = '__all__'
        read_only_fields = ['shared_by', 'created_at']


class StudySessionSerializer(serializers.ModelSerializer):
    notes_count = serializers.IntegerField(source='notes.count', read_only=True)

    class Meta:
        model = StudySession
        fields = '__all__'
        read_only_fields = ['user', 'duration_minutes', 'created_at']


class YouTubeNoteRequestSerializer(serializers.Serializer):
    """Serializer for YouTube note generation requests with validation."""
    url = serializers.URLField(help_text="YouTube video URL")
    title = serializers.CharField(max_length=200, required=False, help_text="Optional custom title")
    category_id = serializers.IntegerField(required=False, help_text="Category ID for organization")
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list, help_text="Tags for categorization")
    is_public = serializers.BooleanField(default=False, help_text="Make note public")

    def validate_url(self, value):
        """Validate that URL is a YouTube URL."""
        if 'youtube.com' not in value and 'youtu.be' not in value:
            raise serializers.ValidationError("URL must be a valid YouTube link.")
        return value


class TextNoteRequestSerializer(serializers.Serializer):
    """Serializer for text-based note generation with validation."""
    text = serializers.CharField(help_text="Text content to summarize")
    title = serializers.CharField(max_length=200, help_text="Title for the note")
    category_id = serializers.IntegerField(required=False, help_text="Category ID")
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list, help_text="Tags")
    is_public = serializers.BooleanField(default=False, help_text="Public flag")

    def validate_text(self, value):
        """Validate text content is not empty."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Text must be at least 10 characters long.")
        return value


class PDFNoteRequestSerializer(serializers.Serializer):
    """Serializer for PDF-based note generation with validation."""
    file = serializers.FileField(help_text="PDF file to process")
    title = serializers.CharField(max_length=200, required=False, help_text="Optional title")
    category_id = serializers.IntegerField(required=False, help_text="Category ID")
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list, help_text="Tags")
    is_public = serializers.BooleanField(default=False, help_text="Public flag")

    def validate_file(self, value):
        """Validate that file is a PDF."""
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("File must be a PDF document.")
        return value
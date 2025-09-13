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
    url = serializers.URLField()
    title = serializers.CharField(max_length=200, required=False)
    category_id = serializers.IntegerField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    is_public = serializers.BooleanField(default=False)


class TextNoteRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    title = serializers.CharField(max_length=200)
    category_id = serializers.IntegerField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    is_public = serializers.BooleanField(default=False)


class PDFNoteRequestSerializer(serializers.Serializer):
    file = serializers.FileField()
    title = serializers.CharField(max_length=200, required=False)
    category_id = serializers.IntegerField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    is_public = serializers.BooleanField(default=False)
# notes/views.py
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ValidationError
import logging
from .models import Note, NoteCategory, NoteShare, StudySession
from .serializers import (
    NoteSerializer, NoteCategorySerializer, NoteCreateSerializer, NoteShareSerializer,
    StudySessionSerializer, YouTubeNoteRequestSerializer, TextNoteRequestSerializer,
    PDFNoteRequestSerializer
)
from .ai_service import NotesAIService

logger = logging.getLogger(__name__)


class NoteCategoryListView(generics.ListCreateAPIView):
    queryset = NoteCategory.objects.all()
    serializer_class = NoteCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Note.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        ).select_related('user', 'category').prefetch_related('likes')

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Filter by tags
        tags = self.request.query_params.get('tags')
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                queryset = queryset.filter(tags__contains=tag.strip())

        # Search in title and content
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        # Filter by source type
        source_type = self.request.query_params.get('source_type')
        if source_type:
            queryset = queryset.filter(source_type=source_type)

        return queryset.distinct()


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        )

    def get_object(self):
        note = super().get_object()
        # Increment view count
        note.views += 1
        note.save(update_fields=['views'])
        return note


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_notes_from_youtube(request):
    """Generate notes from YouTube video URL with comprehensive error handling."""
    serializer = YouTubeNoteRequestSerializer(data=request.data)
    if serializer.is_valid():
        try:
            url = serializer.validated_data['url']
            title = serializer.validated_data.get('title', '')
            category_id = serializer.validated_data.get('category_id')
            tags = serializer.validated_data.get('tags', [])
            is_public = serializer.validated_data.get('is_public', False)

            logger.info(f"Processing YouTube URL: {url}")

            # Generate notes using AI
            ai_result = NotesAIService.process_youtube_url(url, title)

            # Create note object
            note_data = {
                'user': request.user,
                'title': title or ai_result.get('title', 'YouTube Notes'),
                'content': ai_result['content'],
                'summary': ai_result['summary'],
                'source_type': 'youtube',
                'source_url': url,
                'key_points': ai_result.get('key_points', []),
                'questions': ai_result.get('questions', []),
                'difficulty_level': ai_result.get('difficulty_level', 'Medium'),
                'estimated_read_time': ai_result.get('estimated_read_time', 5),
                'tags': tags + ai_result.get('tags', []),
                'is_public': is_public
            }

            if category_id:
                note_data['category_id'] = category_id

            note = Note.objects.create(**note_data)

            # Update user stats
            request.user.total_notes_generated += 1
            request.user.save(update_fields=['total_notes_generated'])

            logger.info(f"Note created successfully: {note.id}")
            return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            logger.error(f"Validation error: {ve}")
            return Response({'error': 'Validation failed', 'details': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error generating YouTube notes: {str(e)}")
            return Response({'error': 'Failed to generate notes', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_notes_from_text(request):
    serializer = TextNoteRequestSerializer(data=request.data)
    if serializer.is_valid():
        try:
            text = serializer.validated_data['text']
            title = serializer.validated_data['title']
            category_id = serializer.validated_data.get('category_id')
            tags = serializer.validated_data.get('tags', [])
            is_public = serializer.validated_data.get('is_public', False)

            # Generate notes using AI
            ai_result = NotesAIService.process_text_input(text, title)

            # Create note object
            note_data = {
                'user': request.user,
                'title': title,
                'content': ai_result['content'],
                'summary': ai_result['summary'],
                'source_type': 'text',
                'key_points': ai_result.get('key_points', []),
                'questions': ai_result.get('questions', []),
                'difficulty_level': ai_result.get('difficulty_level', 'Medium'),
                'estimated_read_time': ai_result.get('estimated_read_time', 5),
                'tags': tags + ai_result.get('tags', []),
                'is_public': is_public
            }

            if category_id:
                note_data['category_id'] = category_id

            note = Note.objects.create(**note_data)

            # Update user stats
            request.user.total_notes_generated += 1
            request.user.save(update_fields=['total_notes_generated'])

            return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_notes_from_pdf(request):
    serializer = PDFNoteRequestSerializer(data=request.data)
    if serializer.is_valid():
        try:
            pdf_file = serializer.validated_data['file']
            title = serializer.validated_data.get('title', '')
            category_id = serializer.validated_data.get('category_id')
            tags = serializer.validated_data.get('tags', [])
            is_public = serializer.validated_data.get('is_public', False)

            # Generate notes using AI
            ai_result = NotesAIService.process_pdf_file(pdf_file, title)

            # Create note object
            note_data = {
                'user': request.user,
                'title': title or ai_result.get('title', 'PDF Notes'),
                'content': ai_result['content'],
                'summary': ai_result['summary'],
                'source_type': 'pdf',
                'source_file': pdf_file,
                'key_points': ai_result.get('key_points', []),
                'questions': ai_result.get('questions', []),
                'difficulty_level': ai_result.get('difficulty_level', 'Medium'),
                'estimated_read_time': ai_result.get('estimated_read_time', 5),
                'tags': tags + ai_result.get('tags', []),
                'is_public': is_public
            }

            if category_id:
                note_data['category_id'] = category_id

            note = Note.objects.create(**note_data)

            # Update user stats
            request.user.total_notes_generated += 1
            request.user.save(update_fields=['total_notes_generated'])

            return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.user in note.likes.all():
        note.likes.remove(request.user)
        liked = False
    else:
        note.likes.add(request.user)
        liked = True

    return Response({
        'liked': liked,
        'likes_count': note.likes.count()
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def share_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Check if user can share this note
    if note.user != request.user and not note.is_public:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = NoteShareSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(note=note, shared_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_shared_notes(request):
    shares = NoteShare.objects.filter(shared_with=request.user).order_by('-created_at')
    serializer = NoteShareSerializer(shares, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enhance_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    try:
        enhancement = NotesAIService.enhance_existing_notes(note.content)
        return Response(enhancement)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudySessionListView(generics.ListCreateAPIView):
    serializer_class = StudySessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudySessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudySessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)
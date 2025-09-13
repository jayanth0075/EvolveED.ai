# views.py for tutor
import json
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Tutor, Session, StudyNote
from .serializers import TutorSerializer, SessionSerializer, StudyNoteSerializer
from .ai_service import TutorAIService


class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="generate-plan")
    def generate_plan(self, request):
        subject = request.data.get("subject")
        current_level = request.data.get("current_level", "beginner")
        target_weeks = request.data.get("target_weeks", 12)

        try:
            ai_response = TutorAIService.generate_study_plan(subject, current_level, target_weeks)
            return Response({"ai_study_plan": json.loads(ai_response)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["post"], url_path="explain-topic")
    def explain_topic(self, request):
        topic = request.data.get("topic")
        try:
            ai_response = TutorAIService.explain_topic(topic)
            return Response({"ai_explanation": json.loads(ai_response)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class StudyNoteViewSet(viewsets.ModelViewSet):
    queryset = StudyNote.objects.all()
    serializer_class = StudyNoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

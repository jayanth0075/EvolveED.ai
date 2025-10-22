# tutor/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class TutorSessionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({"message": "Tutor sessions"})


class ChatMessageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({"message": "Chat messages"})


class ProblemSolvingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({"message": "Problem solving"})


class ConceptExplanationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({"message": "Concept explanations"})


class StudyPlanViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({"message": "Study plans"})


class LearningInsightViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({"message": "Learning insights"})
# roadmaps/views.py
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.utils import timezone
from .models import (
    SkillCategory, Skill, CareerPath, PersonalizedRoadmap,
    RoadmapMilestone, SkillAssessment, LearningResource, UserProgress
)
from .serializers import (
    SkillCategorySerializer, SkillSerializer, SkillListSerializer,
    CareerPathSerializer, CareerPathListSerializer, PersonalizedRoadmapSerializer,
    PersonalizedRoadmapListSerializer, PersonalizedRoadmapCreateSerializer,
    RoadmapMilestoneSerializer, SkillAssessmentSerializer, SkillAssessmentCreateSerializer,
    LearningResourceSerializer, UserProgressSerializer, GenerateRoadmapRequestSerializer,
    SkillGapAnalysisSerializer
)
from .ai_service import RoadmapAIService


class SkillCategoryListView(generics.ListCreateAPIView):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class SkillListView(generics.ListAPIView):
    serializer_class = SkillListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Skill.objects.all().select_related('category')

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        # Filter trending
        trending = self.request.query_params.get('trending')
        if trending == 'true':
            queryset = queryset.filter(is_trending=True)

        # Sort by market demand
        sort_by = self.request.query_params.get('sort', 'name')
        if sort_by == 'demand':
            queryset = queryset.order_by('-market_demand', 'name')
        elif sort_by == 'difficulty':
            difficulty_order = ['beginner', 'intermediate', 'advanced', 'expert']
            queryset = sorted(queryset, key=lambda x: difficulty_order.index(x.difficulty_level))
        else:
            queryset = queryset.order_by('name')

        return queryset


class SkillDetailView(generics.RetrieveAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]


class CareerPathListView(generics.ListAPIView):
    serializer_class = CareerPathListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CareerPath.objects.all().select_related('category')

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        # Filter by salary range
        min_salary = self.request.query_params.get('min_salary')
        if min_salary:
            queryset = queryset.filter(average_salary_min__gte=int(min_salary))

        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Sort options
        sort_by = self.request.query_params.get('sort', 'title')
        if sort_by == 'salary':
            queryset = queryset.order_by('-average_salary_max', 'title')
        elif sort_by == 'growth':
            queryset = queryset.order_by('-job_growth_rate', 'title')
        elif sort_by == 'popular':
            queryset = queryset.order_by('-is_popular', 'title')
        else:
            queryset = queryset.order_by('title')

        return queryset


class CareerPathDetailView(generics.RetrieveAPIView):
    queryset = CareerPath.objects.all()
    serializer_class = CareerPathSerializer
    permission_classes = [permissions.IsAuthenticated]


class PersonalizedRoadmapListView(generics.ListCreateAPIView):
    serializer_class = PersonalizedRoadmapListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = PersonalizedRoadmap.objects.filter(user=self.request.user)

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PersonalizedRoadmapCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PersonalizedRoadmapDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonalizedRoadmapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PersonalizedRoadmap.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_ai_roadmap(request):
    serializer = GenerateRoadmapRequestSerializer(data=request.data)
    if serializer.is_valid():
        try:
            career_goal = serializer.validated_data['career_goal']
            current_skills = serializer.validated_data.get('current_skills', [])
            experience_level = serializer.validated_data['experience_level']
            time_commitment = serializer.validated_data['time_commitment_hours_per_week']
            target_months = serializer.validated_data['target_months']
            learning_style = serializer.validated_data['preferred_learning_style']
            focus_areas = serializer.validated_data.get('focus_areas', [])

            roadmap = RoadmapAIService.generate_personalized_roadmap(
                user=request.user,
                career_goal=career_goal,
                current_skills=current_skills,
                experience_level=experience_level,
                time_commitment=time_commitment,
                target_months=target_months,
                learning_style=learning_style,
                focus_areas=focus_areas
            )

            return Response(
                PersonalizedRoadmapSerializer(roadmap).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def analyze_skill_gaps(request):
    serializer = SkillGapAnalysisSerializer(data=request.data)
    if serializer.is_valid():
        try:
            target_career_path_id = serializer.validated_data['target_career_path_id']
            current_skills_assessment = serializer.validated_data['current_skills_assessment']

            analysis = RoadmapAIService.analyze_skill_gaps(
                user=request.user,
                target_career_path_id=target_career_path_id,
                current_skills_assessment=current_skills_assessment
            )

            return Response(analysis)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_milestone_progress(request, roadmap_id, milestone_id):
    roadmap = get_object_or_404(PersonalizedRoadmap, id=roadmap_id, user=request.user)
    milestone = get_object_or_404(RoadmapMilestone, id=milestone_id, roadmap=roadmap)

    # Update milestone progress
    new_status = request.data.get('status')
    progress_percentage = request.data.get('progress_percentage', 0)
    hours_spent = request.data.get('hours_spent', 0)

    if new_status:
        milestone.status = new_status

        if new_status == 'in_progress' and not milestone.actual_start_date:
            milestone.actual_start_date = timezone.now().date()
        elif new_status == 'completed':
            milestone.actual_completion_date = timezone.now().date()
            milestone.progress_percentage = 100

    if progress_percentage is not None:
        milestone.progress_percentage = min(100, max(0, int(progress_percentage)))

    if hours_spent is not None:
        milestone.actual_hours_spent = int(hours_spent)

    milestone.save()

    # Update overall roadmap progress
    progress_update = RoadmapAIService.update_roadmap_progress(roadmap)

    return Response({
        'milestone': RoadmapMilestoneSerializer(milestone).data,
        'roadmap_progress': progress_update
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def roadmap_analytics(request, roadmap_id):
    roadmap = get_object_or_404(PersonalizedRoadmap, id=roadmap_id, user=request.user)

    milestones = roadmap.milestones.all()
    total_milestones = milestones.count()
    completed_milestones = milestones.filter(status='completed').count()
    in_progress_milestones = milestones.filter(status='in_progress').count()

    # Calculate time metrics
    total_estimated_hours = sum(m.estimated_hours for m in milestones)
    total_actual_hours = sum(m.actual_hours_spent for m in milestones)

    # Calculate completion rate
    completion_rate = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0

    # Time analysis
    days_since_start = (timezone.now().date() - roadmap.start_date).days
    days_remaining = max(0, (roadmap.target_completion_date - timezone.now().date()).days)

    # Progress by skill category
    skill_progress = {}
    for milestone in milestones:
        category = milestone.skill.category.name
        if category not in skill_progress:
            skill_progress[category] = {'completed': 0, 'total': 0}
        skill_progress[category]['total'] += 1
        if milestone.status == 'completed':
            skill_progress[category]['completed'] += 1

    return Response({
        'roadmap_id': roadmap.id,
        'title': roadmap.title,
        'overall_progress': roadmap.overall_progress_percentage,
        'completion_rate': round(completion_rate, 1),
        'milestones': {
            'total': total_milestones,
            'completed': completed_milestones,
            'in_progress': in_progress_milestones,
            'not_started': total_milestones - completed_milestones - in_progress_milestones
        },
        'time_tracking': {
            'estimated_hours': total_estimated_hours,
            'actual_hours': total_actual_hours,
            'days_since_start': days_since_start,
            'days_remaining': days_remaining,
            'efficiency_ratio': round(total_actual_hours / total_estimated_hours, 2) if total_estimated_hours > 0 else 0
        },
        'skill_categories_progress': skill_progress,
        'status': roadmap.status
    })


class SkillAssessmentListView(generics.ListCreateAPIView):
    serializer_class = SkillAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SkillAssessment.objects.filter(user=self.request.user).select_related('skill')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SkillAssessmentCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SkillAssessmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SkillAssessment.objects.filter(user=self.request.user)


class LearningResourceListView(generics.ListAPIView):
    serializer_class = LearningResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = LearningResource.objects.all().prefetch_related('skills')

        # Filter by resource type
        resource_type = self.request.query_params.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)

        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        # Filter by cost
        cost = self.request.query_params.get('cost')
        if cost:
            queryset = queryset.filter(cost=cost)

        # Filter by skills
        skill_ids = self.request.query_params.get('skills')
        if skill_ids:
            skill_id_list = [int(id) for id in skill_ids.split(',')]
            queryset = queryset.filter(skills__id__in=skill_id_list).distinct()

        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Sort by rating or relevance
        sort_by = self.request.query_params.get('sort', 'title')
        if sort_by == 'rating':
            queryset = queryset.order_by('-rating', 'title')
        elif sort_by == 'recommended':
            queryset = queryset.filter(is_recommended=True).order_by('-content_quality_score')
        else:
            queryset = queryset.order_by('title')

        return queryset


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_resource_recommendations(request):
    skill_ids = request.data.get('skill_ids', [])
    learning_style = request.data.get('learning_style', 'mixed')
    difficulty_level = request.data.get('difficulty_level', 'intermediate')

    if not skill_ids:
        return Response({'error': 'skill_ids are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        recommendations = RoadmapAIService.recommend_learning_resources(
            user=request.user,
            skill_ids=skill_ids,
            learning_style=learning_style,
            difficulty_level=difficulty_level
        )

        return Response(recommendations)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProgressListView(generics.ListCreateAPIView):
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = UserProgress.objects.filter(user=self.request.user).select_related('resource', 'roadmap')

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by roadmap
        roadmap_id = self.request.query_params.get('roadmap')
        if roadmap_id:
            queryset = queryset.filter(roadmap_id=roadmap_id)

        return queryset.order_by('-last_accessed')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_resource_progress(request, resource_id):
    resource = get_object_or_404(LearningResource, id=resource_id)

    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        resource=resource,
        defaults={'status': 'not_started'}
    )

    # Update progress
    new_status = request.data.get('status')
    progress_percentage = request.data.get('progress_percentage')
    time_spent = request.data.get('time_spent_minutes')
    rating = request.data.get('rating')
    review = request.data.get('review')

    if new_status:
        progress.status = new_status
        if new_status == 'in_progress' and not progress.started_at:
            progress.started_at = timezone.now()
        elif new_status == 'completed':
            progress.completed_at = timezone.now()
            progress.progress_percentage = 100

    if progress_percentage is not None:
        progress.progress_percentage = min(100, max(0, int(progress_percentage)))

    if time_spent is not None:
        progress.time_spent_minutes += int(time_spent)

    if rating is not None:
        progress.rating = int(rating)

    if review:
        progress.review = review

    progress.save()

    return Response(UserProgressSerializer(progress).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def learning_analytics(request):
    user = request.user

    # Overall learning statistics
    roadmaps = PersonalizedRoadmap.objects.filter(user=user)
    total_roadmaps = roadmaps.count()
    active_roadmaps = roadmaps.filter(status='active').count()
    completed_roadmaps = roadmaps.filter(status='completed').count()

    # Progress statistics
    user_progress = UserProgress.objects.filter(user=user)
    total_resources = user_progress.count()
    completed_resources = user_progress.filter(status='completed').count()
    in_progress_resources = user_progress.filter(status='in_progress').count()

    total_study_time = user_progress.aggregate(
        total_time=models.Sum('time_spent_minutes')
    )['total_time'] or 0

    # Skill assessments
    assessments = SkillAssessment.objects.filter(user=user)
    skill_levels = {}
    for assessment in assessments:
        level = assessment.current_level
        skill_levels[level] = skill_levels.get(level, 0) + 1

    # Recent activity (last 30 days)
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_progress = user_progress.filter(last_accessed__gte=thirty_days_ago).count()

    # Learning streak
    streak_days = 0
    current_date = timezone.now().date()
    for i in range(30):  # Check last 30 days
        check_date = current_date - timedelta(days=i)
        if user_progress.filter(last_accessed__date=check_date).exists():
            streak_days += 1
        else:
            break

    return Response({
        'roadmaps': {
            'total': total_roadmaps,
            'active': active_roadmaps,
            'completed': completed_roadmaps,
            'completion_rate': round((completed_roadmaps / total_roadmaps * 100), 1) if total_roadmaps > 0 else 0
        },
        'resources': {
            'total': total_resources,
            'completed': completed_resources,
            'in_progress': in_progress_resources,
            'completion_rate': round((completed_resources / total_resources * 100), 1) if total_resources > 0 else 0
        },
        'study_time': {
            'total_minutes': total_study_time,
            'total_hours': round(total_study_time / 60, 1),
            'average_per_day': round(total_study_time / 30, 1) if total_study_time > 0 else 0
        },
        'skill_distribution': skill_levels,
        'activity': {
            'recent_activity_count': recent_progress,
            'streak_days': streak_days
        }
    })
# urls.py for roadmaps
# roadmaps/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Skill Categories
    path('categories/', views.SkillCategoryListView.as_view(), name='skill_categories'),

    # Skills
    path('skills/', views.SkillListView.as_view(), name='skill_list'),
    path('skills/<int:pk>/', views.SkillDetailView.as_view(), name='skill_detail'),

    # Career Paths
    path('career-paths/', views.CareerPathListView.as_view(), name='career_path_list'),
    path('career-paths/<int:pk>/', views.CareerPathDetailView.as_view(), name='career_path_detail'),

    # Personalized Roadmaps
    path('', views.PersonalizedRoadmapListView.as_view(), name='roadmap_list'),
    path('<int:pk>/', views.PersonalizedRoadmapDetailView.as_view(), name='roadmap_detail'),

    # AI-powered features
    path('generate/', views.generate_ai_roadmap, name='generate_ai_roadmap'),
    path('skill-gap-analysis/', views.analyze_skill_gaps, name='analyze_skill_gaps'),

    # Milestone Management
    path('<int:roadmap_id>/milestones/<int:milestone_id>/progress/', views.update_milestone_progress,
         name='update_milestone_progress'),

    # Analytics
    path('<int:roadmap_id>/analytics/', views.roadmap_analytics, name='roadmap_analytics'),
    path('analytics/', views.learning_analytics, name='learning_analytics'),

    # Skill Assessments
    path('assessments/', views.SkillAssessmentListView.as_view(), name='skill_assessments'),
    path('assessments/<int:pk>/', views.SkillAssessmentDetailView.as_view(), name='skill_assessment_detail'),

    # Learning Resources
    path('resources/', views.LearningResourceListView.as_view(), name='learning_resources'),
    path('resources/recommendations/', views.get_resource_recommendations, name='resource_recommendations'),
    path('resources/<int:resource_id>/progress/', views.update_resource_progress, name='update_resource_progress'),

    # User Progress
    path('progress/', views.UserProgressListView.as_view(), name='user_progress'),
]
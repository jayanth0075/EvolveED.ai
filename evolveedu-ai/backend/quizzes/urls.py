# quizzes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.QuizCategoryListView.as_view(), name='quiz_categories'),

    # Quiz CRUD
    path('', views.QuizListView.as_view(), name='quiz_list'),
    path('create/', views.QuizCreateView.as_view(), name='quiz_create'),
    path('<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),

    # AI Quiz Generation
    path('generate/', views.generate_quiz_with_ai, name='generate_quiz'),

    # Quiz Attempts
    path('<int:quiz_id>/start/', views.start_quiz_attempt, name='start_quiz_attempt'),
    path('attempts/<int:attempt_id>/submit/', views.submit_quiz_attempt, name='submit_quiz_attempt'),
    path('attempts/<int:attempt_id>/questions/<int:question_id>/respond/', views.submit_quiz_response,
         name='submit_quiz_response'),
    path('attempts/<int:attempt_id>/results/', views.quiz_attempt_results, name='quiz_attempt_results'),
    path('attempts/', views.user_quiz_attempts, name='user_quiz_attempts'),

    # Recommendations
    path('recommendations/', views.quiz_recommendations, name='quiz_recommendations'),
    path('recommendations/<int:recommendation_id>/dismiss/', views.dismiss_recommendation,
         name='dismiss_recommendation'),

    # Analytics
    path('analytics/', views.quiz_analytics, name='quiz_analytics'),
]
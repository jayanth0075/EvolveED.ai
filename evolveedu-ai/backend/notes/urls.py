# notes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.NoteCategoryListView.as_view(), name='note_categories'),

    # Notes CRUD
    path('', views.NoteListView.as_view(), name='note_list'),
    path('<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),

    # AI Note Generation
    path('generate/youtube/', views.generate_notes_from_youtube, name='generate_youtube_notes'),
    path('generate/text/', views.generate_notes_from_text, name='generate_text_notes'),
    path('generate/pdf/', views.generate_notes_from_pdf, name='generate_pdf_notes'),

    # Note Actions
    path('<int:note_id>/like/', views.like_note, name='like_note'),
    path('<int:note_id>/share/', views.share_note, name='share_note'),
    path('<int:note_id>/enhance/', views.enhance_note, name='enhance_note'),

    # Shared Notes
    path('shared/', views.my_shared_notes, name='my_shared_notes'),

    # Study Sessions
    path('sessions/', views.StudySessionListView.as_view(), name='study_sessions'),
    path('sessions/<int:pk>/', views.StudySessionDetailView.as_view(), name='study_session_detail'),
]
# tests.py for roadmaps
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from roadmaps.models import SkillCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="tester", password="pass123")


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


# ------------------
# SkillCategory Tests
# ------------------

@pytest.mark.django_db
def test_create_skill_category(auth_client):
    response = auth_client.post("/api/skill-categories/", {
        "name": "AI",
        "description": "Artificial Intelligence"
    })
    assert response.status_code == 201
    assert response.data["name"] == "AI"


@pytest.mark.django_db
def test_list_skill_categories(auth_client):
    SkillCategory.objects.create(name="Data Science")
    response = auth_client.get("/api/skill-categories/")
    assert response.status_code == 200
    assert len(response.data) >= 1


# ------------------
# Roadmap AI Endpoint
# ------------------

@pytest.mark.django_db
def test_generate_roadmap(auth_client, monkeypatch):
    def fake_ai(prompt, **kwargs):
        return '{"overview": "Test Plan", "milestones": []}'

    monkeypatch.setattr(
        "roadmaps.ai_service.RoadmapAIService._query_hf",
        lambda *a, **kw: fake_ai("x")
    )

    payload = {
        "career_goal": "Data Scientist",
        "current_skills": "Python, Pandas",
        "experience_level": "Beginner",
        "time_commitment_hours_per_week": 10,
        "target_months": 6,
        "preferred_learning_style": "Hands-on",
        "focus_areas": "Machine Learning"
    }
    response = auth_client.post(
        "/api/personalized-roadmaps/generate/",
        payload,
        format="json"
    )
    assert response.status_code == 200
    assert "ai_roadmap" in response.data


# ------------------
# Skill Gap AI Endpoint
# ------------------

@pytest.mark.django_db
def test_analyze_skill_gaps(auth_client, monkeypatch):
    def fake_ai(prompt, **kwargs):
        return '{"missing_skills": ["SQL"], "recommended_resources": ["Khan Academy"]}'

    monkeypatch.setattr(
        "roadmaps.ai_service.RoadmapAIService._query_hf",
        lambda *a, **kw: fake_ai("x")
    )

    payload = {
        "target_career_path": "Data Scientist",
        "current_skills_assessment": "Python, Pandas"
    }
    response = auth_client.post(
        "/api/skill-assessments/analyze-gaps/",
        payload,
        format="json"
    )
    assert response.status_code == 200
    assert "ai_gap_analysis" in response.data

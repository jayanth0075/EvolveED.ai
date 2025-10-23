from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import SkillCategory, Skill, CareerPath

User = get_user_model()


class SkillCategoryUnitTestCase(TestCase):
    """Unit tests for SkillCategory model."""

    def setUp(self):
        """Set up test category."""
        self.category = SkillCategory.objects.create(
            name='Web Development',
            description='Web development skills'
        )

    def test_category_creation(self):
        """Test category creation."""
        self.assertEqual(self.category.name, 'Web Development')
        self.assertEqual(str(self.category), 'Web Development')

    def test_category_unique_name(self):
        """Test category name is unique."""
        with self.assertRaises(Exception):
            SkillCategory.objects.create(name='Web Development')


class SkillUnitTestCase(TestCase):
    """Unit tests for Skill model."""

    def setUp(self):
        """Set up test skill."""
        self.category = SkillCategory.objects.create(name='Programming')
        self.skill = Skill.objects.create(
            name='Python',
            description='Python programming language',
            category=self.category
        )

    def test_skill_creation(self):
        """Test skill creation."""
        self.assertEqual(self.skill.name, 'Python')
        self.assertEqual(self.skill.category, self.category)

    def test_skill_string_representation(self):
        """Test skill string representation."""
        self.assertEqual(str(self.skill), 'Python')


class CareerPathUnitTestCase(TestCase):
    """Unit tests for CareerPath model."""

    def setUp(self):
        """Set up test career path."""
        self.category = SkillCategory.objects.create(name='Technology')
        self.path = CareerPath.objects.create(
            title='Full Stack Developer',
            description='Develop full stack applications',
            category=self.category
        )

    def test_career_path_creation(self):
        """Test career path creation."""
        self.assertEqual(self.path.title, 'Full Stack Developer')
        self.assertFalse(self.path.is_popular)

    def test_career_path_string_representation(self):
        """Test career path string representation."""
        self.assertEqual(str(self.path), 'Full Stack Developer')


# ------------------
# SkillCategory API Tests
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

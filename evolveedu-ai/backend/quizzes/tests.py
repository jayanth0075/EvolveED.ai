from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Quiz, QuizCategory

User = get_user_model()


class QuizCategoryTestCase(TestCase):
    """Test cases for QuizCategory model."""

    def setUp(self):
        """Set up test category."""
        self.category = QuizCategory.objects.create(
            name='Math',
            description='Mathematics'
        )

    def test_category_creation(self):
        """Test category creation."""
        self.assertEqual(self.category.name, 'Math')
        self.assertEqual(str(self.category), 'Math')


class QuizTestCase(TestCase):
    """Test cases for Quiz model."""

    def setUp(self):
        """Set up test user and quiz."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = QuizCategory.objects.create(name='Programming')
        self.quiz = Quiz.objects.create(
            title='Python Basics Quiz',
            description='Test your Python knowledge',
            category=self.category,
            created_by=self.user
        )

    def test_quiz_creation(self):
        """Test quiz creation."""
        self.assertEqual(self.quiz.title, 'Python Basics Quiz')
        self.assertEqual(self.quiz.created_by, self.user)

    def test_quiz_default_values(self):
        """Test quiz default values."""
        self.assertEqual(self.quiz.difficulty_level, 'intermediate')
        self.assertEqual(self.quiz.quiz_type, 'practice')

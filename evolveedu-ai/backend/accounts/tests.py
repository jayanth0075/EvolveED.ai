from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test cases for the User model."""

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        """Test user creation."""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'student')

    def test_user_string_representation(self):
        """Test user string representation."""
        self.assertEqual(str(self.user), 'test@example.com')

    def test_user_role_choices(self):
        """Test user role field."""
        self.assertIn(self.user.role, ['student', 'professional', 'teacher'])


class UserProgressTestCase(TestCase):
    """Test cases for UserProgress model."""

    def setUp(self):
        """Set up test user and progress."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_progress_auto_creation(self):
        """Test that progress is automatically created."""
        self.assertTrue(hasattr(self.user, 'progress'))

    def test_progress_default_values(self):
        """Test progress default values."""
        self.assertEqual(self.user.progress.total_study_time, 0)
        self.assertEqual(self.user.progress.streak_days, 0)

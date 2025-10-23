from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Note, NoteCategory, StudySession

User = get_user_model()


class NoteCategoryTestCase(TestCase):
    """Test cases for NoteCategory model."""

    def setUp(self):
        """Set up test category."""
        self.category = NoteCategory.objects.create(
            name='Python',
            description='Python Programming'
        )

    def test_category_creation(self):
        """Test category creation."""
        self.assertEqual(self.category.name, 'Python')
        self.assertEqual(str(self.category), 'Python')


class NoteTestCase(TestCase):
    """Test cases for Note model."""

    def setUp(self):
        """Set up test user, category and note."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = NoteCategory.objects.create(name='Programming')
        self.note = Note.objects.create(
            user=self.user,
            title='Test Note',
            content='This is a test note',
            source_type='text',
            category=self.category
        )

    def test_note_creation(self):
        """Test note creation."""
        self.assertEqual(self.note.title, 'Test Note')
        self.assertEqual(self.note.user, self.user)

    def test_note_default_values(self):
        """Test note default values."""
        self.assertEqual(self.note.views, 0)
        self.assertFalse(self.note.is_public)
        self.assertEqual(self.note.difficulty_level, 'Medium')

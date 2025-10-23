from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import TutorSession, ChatMessage

User = get_user_model()


class TutorSessionTestCase(TestCase):
    """Test cases for TutorSession model."""

    def setUp(self):
        """Set up test session."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.session = TutorSession.objects.create(
            user=self.user,
            session_type='chat',
            title='Python Learning',
            subject='Python'
        )

    def test_session_creation(self):
        """Test session creation."""
        self.assertEqual(self.session.title, 'Python Learning')
        self.assertEqual(self.session.session_type, 'chat')
        self.assertEqual(self.session.status, 'active')

    def test_session_default_values(self):
        """Test session default values."""
        self.assertTrue(hasattr(self.session, 'started_at'))
        self.assertEqual(self.session.status, 'active')


class ChatMessageTestCase(TestCase):
    """Test cases for ChatMessage model."""

    def setUp(self):
        """Set up test message."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.session = TutorSession.objects.create(
            user=self.user,
            session_type='chat',
            title='Test Session'
        )
        self.message = ChatMessage.objects.create(
            session=self.session,
            message_type='user',
            content='What is Python?'
        )

    def test_message_creation(self):
        """Test message creation."""
        self.assertEqual(self.message.content, 'What is Python?')
        self.assertEqual(self.message.message_type, 'user')

    def test_message_relationships(self):
        """Test message relationships."""
        self.assertEqual(self.message.session, self.session)

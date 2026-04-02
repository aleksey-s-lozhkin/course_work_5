from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты для модели пользователя"""

    def test_create_user_with_email(self):
        """Тест создания пользователя по email"""
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_user_without_email(self):
        """Тест создания пользователя без email (должен быть error)"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, username='testuser', password='testpass123')

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin = User.objects.create_superuser(email='admin@example.com', username='admin', password='adminpass123')
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

    def test_create_superuser_not_staff(self):
        """Тест: суперпользователь должен иметь is_staff=True"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com', username='admin', password='adminpass123', is_staff=False
            )

    def test_user_str_method(self):
        """Тест строкового представления"""
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.assertEqual(str(user), 'test@example.com')

    def test_user_telegram_chat_id(self):
        """Тест поля telegram_chat_id"""
        user = User.objects.create_user(
            email='test@example.com', username='testuser', password='testpass123', telegram_chat_id='123456789'
        )
        self.assertEqual(user.telegram_chat_id, '123456789')

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserViewsTest(TestCase):
    """Тесты для представлений пользователей"""

    def setUp(self):
        self.client = APIClient()
        self.register_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
        }

    def test_register_success(self):
        """Тест успешной регистрации"""
        response = self.client.post('/api/users/register/', self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_register_password_mismatch(self):
        """Тест: пароли не совпадают"""
        self.register_data['password_confirm'] = 'wrong'
        response = self.client.post('/api/users/register/', self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        """Тест: email уже существует"""
        self.client.post('/api/users/register/', self.register_data, format='json')
        response = self.client.post('/api/users/register/', self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_email_available(self):
        """Тест проверки доступного email"""
        response = self.client.post(
            '/api/users/check-email/', {'email': 'new@example.com'}, format='json'
        )  # ✅ Добавлен format='json'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['available'])

    def test_check_email_exists(self):
        """Тест проверки существующего email"""
        self.client.post('/api/users/register/', self.register_data, format='json')
        response = self.client.post('/api/users/check-email/', {'email': 'test@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['available'])

    def test_update_chat_id(self):
        """Тест обновления chat_id"""
        # Сначала регистрируем пользователя
        self.client.post('/api/users/register/', self.register_data, format='json')

        # Получаем токен
        response = self.client.post(
            '/api/users/token/', {'email': 'test@example.com', 'password': 'testpass123'}, format='json'
        )

        self.assertIn('access', response.data)  # ✅ Проверяем наличие токена
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post('/api/users/update-chat-id/', {'telegram_chat_id': '123456789'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['telegram_chat_id'], '123456789')

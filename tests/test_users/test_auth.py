from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserAuthTest(APITestCase):
    """Тесты аутентификации пользователей"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:register')
        self.token_url = reverse('users:token_obtain_pair')
        self.check_email_url = reverse('users:check-email')
        self.profile_url = reverse('users:profile')

        # Создаем тестового пользователя
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')

    def test_register_user(self):
        """Тест регистрации пользователя"""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
        }
        # ✅ Добавляем format='json'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_register_duplicate_email(self):
        """Тест регистрации с существующим email"""
        data = {
            'email': 'test@example.com',  # email уже существует
            'username': 'newuser',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
        }
        # ✅ Добавляем format='json'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch(self):
        """Тест регистрации с несовпадающими паролями"""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'StrongPass123!',
            'password_confirm': 'WrongPass123!',
        }
        # ✅ Добавляем format='json'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_confirm', response.data)

    def test_token_obtain(self):
        """Тест получения JWT токена"""
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        # ✅ Добавляем format='json'
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_obtain_invalid_credentials(self):
        """Тест получения токена с неверными данными"""
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        # ✅ Добавляем format='json'
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_view(self):
        """Тест получения профиля"""
        # Получаем токен
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # ✅ Авторизуемся
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_check_email_available(self):
        """Тест проверки доступного email"""
        data = {'email': 'newuser@example.com'}
        # ✅ Добавляем format='json'
        response = self.client.post(self.check_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['exists'], False)
        self.assertEqual(response.data['available'], True)

    def test_check_email_exists(self):
        """Тест проверки существующего email"""
        data = {'email': 'test@example.com'}
        # ✅ Добавляем format='json'
        response = self.client.post(self.check_email_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['exists'], True)
        self.assertEqual(response.data['available'], False)

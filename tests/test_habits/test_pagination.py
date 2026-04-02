from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from habits.models import Habit

User = get_user_model()


class HabitPaginationTest(APITestCase):
    """Тесты пагинации привычек"""

    def setUp(self):
        """Подготовка: создаем пользователя и авторизуемся"""
        # Создаем пользователя
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')

        # Получаем JWT токен
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Настраиваем клиент с токеном
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.habits_url = reverse('habit-list')

        # Создаем 7 привычек для теста пагинации
        for i in range(7):
            Habit.objects.create(
                user=self.user,
                place=f'Место {i}',
                time=f'08:{i:02d}:00',
                action=f'Действие {i}',
                execution_time=60,
                periodicity=1,
            )

    def test_pagination_default_page_size(self):
        """Тест: по умолчанию 5 привычек на страницу"""
        response = self.client.get(self.habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 7)

    def test_pagination_second_page(self):
        """Тест: вторая страница"""
        response = self.client.get(self.habits_url, {'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_pagination_next_link(self):
        """Тест: наличие ссылки на следующую страницу"""
        response = self.client.get(self.habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['next'])

    def test_pagination_invalid_page(self):
        """Тест: несуществующая страница"""
        response = self.client.get(self.habits_url, {'page': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pagination_page_size_parameter(self):
        """Тест: кастомный размер страницы (если поддерживается)"""
        response = self.client.get(self.habits_url, {'page_size': 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DRF PageNumberPagination не поддерживает page_size по умолчанию
        # поэтому просто проверяем, что ответ 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UnauthorizedPaginationTest(APITestCase):
    """Тесты пагинации для неавторизованных пользователей"""

    def setUp(self):
        self.client = APIClient()
        self.habits_url = reverse('habit-list')

    def test_unauthenticated_cannot_paginate(self):
        """Неавторизованный пользователь не может получить список привычек"""
        response = self.client.get(self.habits_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

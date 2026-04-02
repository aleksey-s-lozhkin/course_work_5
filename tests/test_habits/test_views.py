from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from habits.models import Habit

User = get_user_model()


class HabitAPITest(APITestCase):
    """Тесты API для привычек"""

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

    def test_get_habits_empty(self):
        """Тест получения пустого списка привычек"""
        response = self.client.get(self.habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_create_habit(self):
        """Тест создания привычки"""
        data = {
            'place': 'Дом',
            'time': '08:00:00',
            'action': 'Сделать зарядку',
            'execution_time': 60,
            'periodicity': 1,
        }
        response = self.client.post(self.habits_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_habit_invalid_execution_time(self):
        """Тест создания привычки с невалидным временем выполнения (>120 сек)"""
        data = {
            'place': 'Дом',
            'time': '08:00:00',
            'action': 'Сделать зарядку',
            'execution_time': 150,  # > 120
            'periodicity': 1,
        }
        response = self.client.post(self.habits_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_habit(self):
        """Тест обновления привычки"""
        # Создаем привычку
        habit = Habit.objects.create(
            user=self.user, place='Дом', time='08:00:00', action='Зарядка', execution_time=60, periodicity=1
        )

        url = reverse('habit-detail', args=[habit.id])
        data = {'action': 'Утренняя зарядка'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_habit(self):
        """Тест удаления привычки"""
        habit = Habit.objects.create(
            user=self.user, place='Дом', time='08:00:00', action='Зарядка', execution_time=60, periodicity=1
        )

        url = reverse('habit-detail', args=[habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_see_others_habits(self):
        """Тест: пользователь не видит чужие привычки"""
        # Создаем другого пользователя и его привычку
        other_user = User.objects.create_user(email='other@example.com', username='otheruser', password='otherpass123')
        Habit.objects.create(
            user=other_user, place='Офис', time='09:00:00', action='Работа', execution_time=60, periodicity=1
        )

        # Первый пользователь не видит привычку второго
        response = self.client.get(self.habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

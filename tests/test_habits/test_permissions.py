from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly

User = get_user_model()


class HabitPermissionsTest(TestCase):
    """Тесты для прав доступа к привычкам"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(email='owner@example.com', username='owner', password='testpass123')
        self.other_user = User.objects.create_user(email='other@example.com', username='other', password='testpass123')
        self.habit = Habit.objects.create(
            user=self.user, place='Дом', time='08:00:00', action='Привычка', execution_time=60, periodicity=1
        )

    def test_owner_has_permission(self):
        """Тест: владелец имеет доступ"""
        request = self.factory.get(f'/habits/{self.habit.id}/')
        request.user = self.user
        permission = IsOwnerOrReadOnly()
        result = permission.has_object_permission(request, None, self.habit)
        self.assertTrue(result)

    def test_other_user_no_permission(self):
        """Тест: другой пользователь не имеет доступа"""
        request = self.factory.put(f'/habits/{self.habit.id}/')
        request.user = self.other_user
        permission = IsOwnerOrReadOnly()
        result = permission.has_object_permission(request, None, self.habit)
        self.assertFalse(result)

    def test_safe_methods_allow_anyone(self):
        """Тест: безопасные методы (GET) разрешены всем"""
        request = self.factory.get(f'/habits/{self.habit.id}/')
        request.user = self.other_user
        permission = IsOwnerOrReadOnly()
        result = permission.has_object_permission(request, None, self.habit)
        self.assertTrue(result)

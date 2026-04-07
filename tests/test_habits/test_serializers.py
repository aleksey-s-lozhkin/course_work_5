from django.contrib.auth import get_user_model
from django.test import TestCase

from habits.serializers import HabitSerializer

User = get_user_model()


class HabitSerializerTest(TestCase):
    """Тесты для сериализатора Habit"""

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.habit_data = {
            'place': 'Дом',
            'time': '08:00:00',
            'action': 'Сделать зарядку',
            'execution_time': 60,
            'periodicity': 1,
        }

    def test_habit_serializer_valid(self):
        """Тест валидного сериализатора"""
        serializer = HabitSerializer(data=self.habit_data)
        self.assertTrue(serializer.is_valid())

    def test_habit_serializer_execution_time_too_long(self):
        """Тест: невалидное время выполнения"""
        self.habit_data['execution_time'] = 150
        serializer = HabitSerializer(data=self.habit_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('execution_time', serializer.errors)

    def test_habit_serializer_periodicity_too_high(self):
        """Тест: невалидная периодичность"""
        self.habit_data['periodicity'] = 10
        serializer = HabitSerializer(data=self.habit_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('periodicity', serializer.errors)

    def test_habit_serializer_create_with_user(self):
        """Тест создания привычки через сериализатор"""
        serializer = HabitSerializer(data=self.habit_data)
        self.assertTrue(serializer.is_valid())
        habit = serializer.save(user=self.user)
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.action, 'Сделать зарядку')

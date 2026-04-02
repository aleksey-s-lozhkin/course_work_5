from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты для модели Habit"""

    def setUp(self):
        """Создание тестового пользователя перед каждым тестом"""
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')

    def test_create_habit(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            user=self.user, place='Дом', time='08:00:00', action='Сделать зарядку', execution_time=60, periodicity=1
        )
        self.assertEqual(habit.action, 'Сделать зарядку')
        self.assertEqual(habit.place, 'Дом')
        self.assertEqual(habit.execution_time, 60)
        self.assertFalse(habit.is_pleasant)

    def test_habit_str_method(self):
        """Тест строкового представления привычки"""
        habit = Habit.objects.create(
            user=self.user, place='Офис', time='14:00:00', action='Прогулка', execution_time=30, periodicity=1
        )
        expected_str = f"{self.user.username}: Прогулка в 14:00:00"
        self.assertEqual(str(habit), expected_str)

    def test_habit_ordering(self):
        """Тест сортировки привычек по дате создания"""
        habit1 = Habit.objects.create(
            user=self.user, place='Дом', time='08:00:00', action='Привычка 1', execution_time=60, periodicity=1
        )
        habit2 = Habit.objects.create(
            user=self.user, place='Дом', time='09:00:00', action='Привычка 2', execution_time=60, periodicity=1
        )
        habits = Habit.objects.all()
        self.assertEqual(habits[0], habit2)  # Более новая должна быть первой
        self.assertEqual(habits[1], habit1)


class HabitValidatorsTest(TestCase):
    """Тесты для валидаторов привычек"""

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')

    def test_validate_execution_time_too_long(self):
        """Тест: время выполнения не должно превышать 120 секунд"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            execution_time=150,  # Превышает 120
            periodicity=1,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_validate_execution_time_valid(self):
        """Тест: валидное время выполнения"""
        habit = Habit(user=self.user, place='Дом', time='08:00:00', action='Зарядка', execution_time=60, periodicity=1)
        try:
            habit.full_clean()
        except ValidationError:
            self.fail("Валидация не должна была вызвать ошибку")

    def test_validate_periodicity_too_high(self):
        """Тест: периодичность не должна превышать 7 дней"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Зарядка',
            execution_time=60,
            periodicity=10,  # Превышает 7
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_validate_reward_and_related_habit(self):
        """Тест: нельзя одновременно указать полезная и приятная привычка"""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Приятная привычка',
            execution_time=30,
            periodicity=1,
            is_pleasant=True,
        )
        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Полезная привычка',
            execution_time=60,
            periodicity=1,
            reward='Шоколадка',
            related_habit=pleasant_habit,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_validate_related_habit_must_be_pleasant(self):
        """Тест: связанная привычка должна быть приятной"""
        unpleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Неприятная привычка',
            execution_time=30,
            periodicity=1,
            is_pleasant=False,
        )
        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Полезная привычка',
            execution_time=60,
            periodicity=1,
            related_habit=unpleasant_habit,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_validate_pleasant_habit_no_reward(self):
        """Тест: у приятной привычки не может быть вознаграждения"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Приятная привычка',
            execution_time=30,
            periodicity=1,
            is_pleasant=True,
            reward='Награда',
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

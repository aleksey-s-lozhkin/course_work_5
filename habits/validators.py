from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class HabitValidators:
    """Класс с валидаторами для привычек"""

    @staticmethod
    def validate_reward_and_related(habit):
        """Исключить одновременный выбор связанной привычки и вознаграждения"""
        if habit.reward and habit.related_habit:
            raise ValidationError(
                _('Нельзя одновременно указывать вознаграждение и связанную привычку')
            )

    @staticmethod
    def validate_execution_time(habit):
        """Время выполнения не должно превышать 120 секунд"""
        if habit.execution_time > 120:
            raise ValidationError(
                _('Время выполнения не должно превышать 120 секунд')
            )

    @staticmethod
    def validate_related_habit(habit):
        """Связанная привычка может быть только приятной"""
        if habit.related_habit and not habit.related_habit.is_pleasant:
            raise ValidationError(
                _('Связанная привычка должна быть приятной')
            )

    @staticmethod
    def validate_pleasant_habit(habit):
        """У приятной привычки не может быть вознаграждения или связанной привычки"""
        if habit.is_pleasant:
            if habit.reward or habit.related_habit:
                raise ValidationError(
                    _('Приятная привычка не может иметь вознаграждение или связанную привычку')
                )

    @staticmethod
    def validate_periodicity(habit):
        """Периодичность не должна быть больше 7 дней"""
        if habit.periodicity > 7:
            raise ValidationError(
                _('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')
            )

    @classmethod
    def validate_all(cls, habit):
        """Применить все валидаторы"""
        cls.validate_reward_and_related(habit)
        cls.validate_execution_time(habit)
        cls.validate_related_habit(habit)
        cls.validate_pleasant_habit(habit)
        cls.validate_periodicity(habit)
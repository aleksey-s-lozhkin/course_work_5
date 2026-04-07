from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычек"""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate(self, data):
        """Валидация через модель. Не дублируем логику!"""
        # Создаем объект для валидации
        if self.instance:
            habit = self.instance
            for key, value in data.items():
                setattr(habit, key, value)
        else:
            habit = Habit(**data)

        # Вызываем валидацию модели
        try:
            habit.clean()
        except DjangoValidationError as e:
            # Django ValidationError с error_dict
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(dict(e))
            # Django ValidationError с error_list
            elif hasattr(e, 'error_list'):
                errors = {}
                for err in e.error_list:
                    if hasattr(err, 'message'):
                        errors.setdefault('non_field_errors', []).append(err.message)
                raise serializers.ValidationError(errors)
            else:
                raise serializers.ValidationError({'non_field_errors': [str(e)]})

        return data

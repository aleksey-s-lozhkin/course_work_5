from rest_framework import serializers
from .models import Habit
from .validators import HabitValidators


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычек"""
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate(self, data):
        """Комплексная валидация"""

        # Создаем временный объект для валидации
        instance = Habit(**data) if not self.instance else self.instance

        # Обновляем атрибуты для валидации
        for key, value in data.items():
            setattr(instance, key, value)

        # Применяем все валидаторы
        HabitValidators.validate_all(instance)

        return data
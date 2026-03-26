from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычек"""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate(self, data):
        """ Валидация через модель. Не дублируем логику! """
        # Создаем объект для валидации
        if self.instance:
            # Обновление существующего
            habit = self.instance
            for key, value in data.items():
                setattr(habit, key, value)
        else:
            # Создание нового
            habit = Habit(**data)

        # Вызываем валидацию модели
        try:
            habit.clean()
        except ValidationError as e:
            # Преобразуем ошибки модели в ошибки сериализатора
            raise serializers.ValidationError(e.message_dict)

        return data
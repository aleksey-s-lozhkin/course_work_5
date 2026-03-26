from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly, IsPublicHabitReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками"""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Пользователь видит только свои привычки"""
        if not self.request.user.is_authenticated:
            return Habit.objects.none()
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании привязываем привычку к пользователю"""
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """Переопределяем list для корректной обработки пустого списка"""
        queryset = self.filter_queryset(self.get_queryset())

        # Пагинация
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='public')
    def list_public(self, request):
        """Список публичных привычек"""
        public_habits = Habit.objects.filter(is_public=True)

        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)

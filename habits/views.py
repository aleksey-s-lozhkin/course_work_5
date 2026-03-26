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
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании привязываем привычку к пользователю"""
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_path='public',
        permission_classes=[permissions.IsAuthenticated]
    )

    def public_habits(self, request):
        """ Список публичных привычек. Доступен всем аутентифицированным пользователям. """
        public_habits = Habit.objects.filter(is_public=True)

        # Пагинация
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)

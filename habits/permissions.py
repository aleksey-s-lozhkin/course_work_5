from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение на редактирование только владельцу.
    Для публичных привычек - только чтение."""

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Изменять может только владелец
        return obj.user == request.user


class IsPublicHabitReadOnly(permissions.BasePermission):
    """Для публичных привычек - только чтение."""

    def has_permission(self, request, view):
        # Для списка публичных привычек
        if view.action == 'public_habits':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        # Публичные привычки можно только читать
        if obj.is_public and request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

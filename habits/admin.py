from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Админка для привычек"""

    list_display = ('action', 'user', 'time', 'place', 'is_pleasant', 'is_public')
    list_filter = ('is_pleasant', 'is_public', 'periodicity')
    search_fields = ('action', 'place', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {'fields': ('user', 'action', 'place', 'time')}),
        ('Тип привычки', {'fields': ('is_pleasant', 'related_habit', 'reward')}),
        ('Настройки', {'fields': ('periodicity', 'execution_time', 'is_public')}),
        ('Системные поля', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

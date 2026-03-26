from django.contrib import admin
from .models import TelegramNotification

@admin.register(TelegramNotification)
class TelegramNotificationAdmin(admin.ModelAdmin):
    """Админка для уведомлений"""
    list_display = ('user', 'habit', 'sent_at', 'is_success')
    list_filter = ('is_success', 'sent_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('sent_at',)
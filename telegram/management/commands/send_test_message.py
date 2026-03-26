from django.core.management.base import BaseCommand
from telegram.utils import send_telegram_message


class Command(BaseCommand):
    help = 'Отправка тестового сообщения в Telegram'

    def add_arguments(self, parser):
        parser.add_argument('chat_id', type=str, help='Telegram chat ID')
        parser.add_argument('message', type=str, help='Текст сообщения')

    def handle(self, *args, **options):
        chat_id = options['chat_id']
        message = options['message']

        self.stdout.write(f"Отправка сообщения в chat_id={chat_id}...")

        success = send_telegram_message(chat_id, message)

        if success:
            self.stdout.write(self.style.SUCCESS('✅ Сообщение отправлено успешно!'))
        else:
            self.stdout.write(self.style.ERROR('❌ Ошибка отправки сообщения'))
import asyncio

from django.core.management.base import BaseCommand
from server.bot import main  # Импорт функции main из bot.py


class Command(BaseCommand):
    help = 'Start the Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting bot...'))
        asyncio.run(main())

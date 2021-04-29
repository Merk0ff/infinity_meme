from django.core.management.base import BaseCommand

from storage.models import LocalStorage


class Command(BaseCommand):
    help = 'My custom startup command'

    def handle(self, *args, **kwargs):
        LocalStorage.objects.create(
            name='local',
            capacity=1024*1024*50,
            base_path='/meme-data'
        )

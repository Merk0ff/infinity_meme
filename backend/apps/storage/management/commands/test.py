from django.core.management.base import BaseCommand

from parsers.tasks import download_memes


class Command(BaseCommand):
    help = 'My custom startup command'

    def add_arguments(self, parser):
        parser.add_argument('meme_count', nargs='?', default=30)

    def handle(self, *args, **kwargs):
        download_memes.apply_async(args=[kwargs['meme_count']])

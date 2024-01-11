
from django.core.management.base import BaseCommand
from base.models import News
from django.utils import timezone

class Command(BaseCommand):
    help = 'Adds a new news item to the database'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('link', type=str)
        parser.add_argument('image_url', type=str)
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        News.objects.create(
            title=options['title'],
            description=options['description'],
            content=options['content'],
            link=options['link'],
            image_url=options['image_url'],
            published_time=timezone.now(),
            category=options['category']
        )
        self.stdout.write(self.style.SUCCESS('Successfully added news item!'))

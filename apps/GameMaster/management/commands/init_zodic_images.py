from django.core.management.base import BaseCommand

from apps.GameMaster.models import ZodiacImage

from apps.GameMaster.constants import ZODIAC_CHOICES


class Command(BaseCommand):
    help = "Init Zodic Images"

    def handle(self, *args, **options):
        for zodiac in ZODIAC_CHOICES:
            name = zodiac[0]
            zodiac_image, created = ZodiacImage.objects.get_or_create(name=name, image_url='/static/img/' + name +'.gif')
            print(created, zodiac_image)
            
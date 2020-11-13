from django.core.management.base import BaseCommand

from apps.GameMaster.models import Character
from apps.GameMaster.constants import CHARACTOR_CHOICES


class Command(BaseCommand):
    help = "Init Characters"

    def handle(self, *args, **options):
        for char in CHARACTOR_CHOICES:
            name = char[0]
            character, created = Character.objects.get_or_create(name=name)
            print(created, character)
            
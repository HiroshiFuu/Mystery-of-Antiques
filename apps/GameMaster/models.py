from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from apps.GameMaster.constants import CHARACTOR_CHOICES, COLOR_CHOICES, ZODIAC_CHOICES, ZODIAC_STATUS_CHOICES

from datetime import timedelta
import os

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "r"
en_formats.DATE_FORMAT = "d M Y"
en_formats.TIME_FORMAT = "H:i:s"


# Create your models here.
class LogMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        editable=False, auto_now_add=True, verbose_name='Created At')
    modified_at = models.DateTimeField(
        editable=False, blank=True, null=True, verbose_name='Modified At')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)


class Game(LogMixin):
	room_id = models.PositiveSmallIntegerField(
		unique=True, help_text="Room Number", verbose_name='Room ID')
	stage = models.SmallIntegerField(default=-1)
	start_color_index = models.PositiveSmallIntegerField()

	class Meta:
		# 	verbose_name = '玩家'
		# 	verbose_name_plural = '玩家'
		ordering = ['-created_at',]

	def __str__(self):
		return 'Room Number: %s  Stage: %s' % (self.room_id, self.stage)


class ZodiacImage(LogMixin):
	name = models.CharField(max_length=31, choices=ZODIAC_CHOICES, unique=True)
	image_url = models.CharField(max_length=127, unique=True)

	class Meta:
		# 	verbose_name = '玩家'
		# 	verbose_name_plural = '玩家'
		ordering = ['name']

	def __str__(self):
		return 'Name: %s  ImageURL: %s' % (self.name, self.image_url)

	def image_tag(self):
		return mark_safe(u'<img src="%s" />' % self.image_url)
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True


class Zodiac(LogMixin):
	name = models.CharField(max_length=31, choices=ZODIAC_CHOICES)
	genuine = models.BooleanField(default=True, verbose_name='真伪')
	sequence = models.PositiveSmallIntegerField(null=True)
	status = models.PositiveSmallIntegerField(choices=ZODIAC_STATUS_CHOICES, default=0)
	zodiac_image = models.ForeignKey(ZodiacImage, models.PROTECT, related_name='zodiacs', verbose_name='Zodiac Image')
	game = models.ForeignKey(Game, models.CASCADE, related_name='zodiacs')

	def __str__(self):
		return 'Room Number: %s  Name: %s  Genuine: %s  Sequence: %s' % (self.game.room_id, self.name, self.genuine, self.sequence)

	class Meta:
		# 	verbose_name = '玩家'
		# 	verbose_name_plural = '玩家'
		ordering = ['game', 'sequence']


class Character(LogMixin):
	name = models.CharField(
		max_length=31, choices=CHARACTOR_CHOICES, unique=True)
	skill_description = models.CharField(max_length=1023, null=True)

	def __str__(self):
		return self.get_name_display()


class Player(LogMixin):
	name = models.CharField(max_length=255)
	player_code = models.PositiveSmallIntegerField(unique=True, help_text="Player Code", verbose_name='Player Code')
	color = models.CharField(max_length=7, choices=COLOR_CHOICES, null=True)
	sequence = models.PositiveSmallIntegerField(default=999)
	step = models.PositiveSmallIntegerField(default=0)
	game = models.ForeignKey(Game, models.CASCADE, related_name='players')
	character = models.ForeignKey(Character, models.PROTECT, verbose_name='Character')

	class Meta:
		# 	verbose_name = '玩家'
		# 	verbose_name_plural = '玩家'
		unique_together = (('game', 'color'), ('game', 'character'))
		ordering = ['game', 'color']

	def __str__(self):
		return 'Name: %s  Character: %s' % (self.name, self.character)

	def is_alive(self):
		return self.modified_at >= timezone.now() - timedelta(seconds=8)
	is_alive.boolean = True
	is_alive.short_description = 'Is Alive?'


class PlayerAction(LogMixin):
	game = models.ForeignKey(Game, models.PROTECT, related_name='actions')
	player = models.ForeignKey(Player, models.PROTECT, related_name='actions')
	character = models.ForeignKey(Character, models.PROTECT, related_name='actions')
	zodic = models.ForeignKey(Zodiac, models.PROTECT, related_name='actions')
	skill_used = models.BooleanField(null=True)
	game_progress = models.PositiveSmallIntegerField(default=-1)

	class Meta:
		# 	verbose_name = '玩家'
		# 	verbose_name_plural = '玩家'
		ordering = ['game', 'game_progress']

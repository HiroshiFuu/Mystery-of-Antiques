from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from .base_model import SlugMixin, AuditMixin
from .base_model import CHARACTOR_CHOICES, COLOR_CHOICES, ZODIAC_CHOICES, ZODIAC_STATUS_CHOICES

from datetime import timedelta
import os
import logging
logger = logging.getLogger(__name__)

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "r"
en_formats.DATE_FORMAT = "d M Y"
en_formats.TIME_FORMAT = "H:i:s"


# Create your models here.
class Game(AuditMixin, models.Model):
	class Meta:
		# 	verbose_name = '玩家'
		# 	verbose_name_plural = '玩家'
		ordering = ['-created_at',]

	room_id = models.PositiveSmallIntegerField(
		unique=True, help_text="Room Number", verbose_name='Room ID')
	stage = models.PositiveSmallIntegerField(default=-1)
	start_color_index = models.PositiveSmallIntegerField(null=True)
	characters = models.ManyToManyField('Character', blank=True)

	def __str__(self):
		return 'Room Number: %s  Stage: %s' % (self.room_id, self.stage)


class ZodiacImage(SlugMixin, AuditMixin, models.Model):
	name = models.CharField(max_length=31, choices=ZODIAC_CHOICES, unique=True)
	image = models.FileField(upload_to='Images/', blank=True, null=True)

	def __str__(self):
		return 'Name: %s  ImagePath: %s' % (self.name, self.image)

	def get_image_name(self):
		return os.path.basename(self.image.name)

	def image_tag(self):
		return mark_safe(u'<img src="%s" />' % self.image.url)
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True


class Zodiac(SlugMixin, AuditMixin, models.Model):
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
		ordering = ['sequence']


class Character(SlugMixin, AuditMixin, models.Model):
	name = models.CharField(
		max_length=31, choices=CHARACTOR_CHOICES, unique=True)
	skill_description = models.CharField(max_length=1023, null=True)

	def __str__(self):
		return self.get_name_display()


class Player(SlugMixin, AuditMixin, models.Model):
	class Meta:
		# 	verbose_name = '玩家'
		# 	verbose_name_plural = '玩家'
		unique_together = (('game', 'color'), ('game', 'character'))
		ordering = ['game', 'color']

	name = models.CharField(max_length=255)
	player_code = models.PositiveSmallIntegerField(unique=True, help_text="Player Code", verbose_name='Player Code')
	color = models.CharField(max_length=7, choices=COLOR_CHOICES, null=True)
	sequence = models.PositiveSmallIntegerField(default=100)
	step = models.PositiveSmallIntegerField(default=0)
	game = models.ForeignKey(Game, models.CASCADE, related_name='players')
	character = models.ForeignKey(Character, models.PROTECT, verbose_name='Character')

	def is_alive(self):
		return self.modified_at >= timezone.now() - timedelta(seconds=8)
	is_alive.boolean = True
	is_alive.short_description = 'Is Alive?'


class PlayerAction(AuditMixin, models.Model):		
	skill_used = models.BooleanField(null=True)
	game = models.ForeignKey(Game, models.PROTECT, related_name='actions')
	player = models.ForeignKey(Player, models.PROTECT, related_name='actions')
	zodic = models.ForeignKey(Zodiac, models.PROTECT, related_name='actions')
	character = models.ForeignKey(Character, models.PROTECT, related_name='actions')

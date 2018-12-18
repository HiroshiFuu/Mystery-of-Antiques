from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext as _

from MysteryOfAntiques.middleware import get_current_user

from django.utils import timezone
from datetime import timedelta
import itertools
import logging
logger = logging.getLogger(__name__)

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "r"
en_formats.DATE_FORMAT = "d M Y"
en_formats.TIME_FORMAT = "H:i:s"

CHARACTOR_CHOICES = {
	('XuYuan', _("许愿")),
	('FanZhen', _("方震")),
	('JiYunFu', _("姬云浮")),
	('Kana Kinoshi', _("木户加奈")),
	('HuanYanYan', _("黄烟烟")),
	('LaoChaoFeng', _("老朝奉")),
	('YaoBuRan', _("药不然")),
	('ZhengGuoQu', _("郑国渠")),
}

COLOR_CHOICES = {
	('Black', _("黑")),
	('White', _("白")),
	('Yellow', _("黄")),
	('Red', _("红")),
	('Green', _("绿")),
	('Orange', _("橙")),
	('Blue', _("蓝")),
	('Purple', _("紫")),
}

ZODIAC_CHOICES = {
	('Rat', _("鼠")),
	('Ox', _("牛")),
	('Tiger', _("虎")),
	('Rabbit', _("兔")),
	('Dragon', _("龙")),
	('Snake', _("蛇")),
	('Horse', _("马")),
	('Sheep', _("羊")),
	('Monkey', _("猴")),
	('Rooster', _("鸡")),
	('Dog', _("狗")),
	('Pig', _("猪")),
}

# Create your models here.
class SlugMixin(models.Model):
	"""
	SlugMixin requires the inherited class to have a "name" field
	"""

	class Meta:
		abstract = True

	slug = models.SlugField(editable=False)

	@classmethod
	def create_slug(cls):
		cls.slug = original = slugify(cls.name)
		for x in itertools.count(1):
			if not cls._meta.model.objects.filter(slug=cls.slug).exists():
				break
			cls.slug = '{}-{}'.format(original, x)

	def save(self, *args, **kwargs):
		if not self.pk:
			self.create_slug()
		super().save(*args, **kwargs)


class AuditMixin(models.Model):

	class Meta:
		abstract = True

	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
								   models.PROTECT,
								   related_name='%(app_label)s_%(class)s_created_by',
								   editable=False,
								   blank=True,
								   null=True,
								   help_text='Who created this record')
	modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
									models.PROTECT,
									related_name='%(app_label)s_%(class)s_modified_by',
									editable=False,
									blank=True,
									null=True,
									help_text='Who modified this record')

	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			if not self.pk:
				self.created_by = user
			self.modified_by = user
		return super().save(*args, **kwargs)


class Zodiac(SlugMixin, AuditMixin, models.Model):
	name = models.CharField(max_length=31, choices=ZODIAC_CHOICES, unique=True)


class Game(AuditMixin, models.Model):
	room_id = models.PositiveSmallIntegerField(
		unique=True, help_text="Room Number", verbose_name='Room ID')
	stage = models.PositiveSmallIntegerField(default=0, verbose_name='Stage')
	characters = models.ManyToManyField('Character', blank=True)

	def __str__(self):
		return 'Room Number: %s  Stage: %s' % (self.room_id, self.stage)


class Character(SlugMixin, AuditMixin, models.Model):
	name = models.CharField(max_length=31, choices=CHARACTOR_CHOICES, unique=True)
	skill_description = models.CharField(max_length=1023, null=True)

	def __str__(self):
		return self.get_name_display()


class Player(SlugMixin, AuditMixin, models.Model):
	name = models.CharField(max_length=255, unique=True)
	player_code = models.PositiveSmallIntegerField(
		unique=True, help_text="Player Code", verbose_name='Player Code')
	color = models.CharField(max_length=7, choices=COLOR_CHOICES, null=True)
	game = models.ForeignKey(Game, models.PROTECT, related_name='players', verbose_name='Game')
	character = models.ForeignKey(Character, models.PROTECT, verbose_name='Character')

	def is_alive(self):
		return self.modified_at >= timezone.now() - timedelta(seconds=8)
	is_alive.boolean = True
	is_alive.short_description = 'Is Alive?'

	class Meta:
	# 	verbose_name = '玩家'
	# 	verbose_name_plural = '玩家'
		unique_together = (('game', 'color'), ('game', 'character'))
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext as _

from core.middleware import get_current_user

import itertools

CHARACTOR_CHOICES = {
	('XuYuan', _("许愿")),
	('FangZhen', _("方震")),
	('JiYunFu', _("姬云浮")),
	('Kana Kinoshi', _("木户加奈")),
	('HuangYanYan', _("黄烟烟")),
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

ZODIAC_STATUS_CHOICES = {
	(0, _("Normal")),
	(1, _("Inverted")),
	(2, _("Blocked")),
}


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
	# created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
	# 							   models.PROTECT,
	# 							   related_name='%(app_label)s_%(class)s_created_by',
	# 							   editable=False,
	# 							   blank=True,
	# 							   null=True,
	# 							   help_text='Who created this record')
	# modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
	# 								models.PROTECT,
	# 								related_name='%(app_label)s_%(class)s_modified_by',
	# 								editable=False,
	# 								blank=True,
	# 								null=True,
	# 								help_text='Who modified this record')

	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			if not self.pk:
				self.created_by = user
			self.modified_by = user
		return super().save(*args, **kwargs)


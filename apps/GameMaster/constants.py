from django.utils.translation import gettext as _

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
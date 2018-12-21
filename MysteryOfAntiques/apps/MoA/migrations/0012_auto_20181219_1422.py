# Generated by Django 2.1.4 on 2018-12-19 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoA', '0011_auto_20181219_1005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zodiac',
            old_name='image',
            new_name='zodiac_image',
        ),
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(choices=[('YaoBuRan', '药不然'), ('FanZhen', '方震'), ('JiYunFu', '姬云浮'), ('HuanYanYan', '黄烟烟'), ('ZhengGuoQu', '郑国渠'), ('LaoChaoFeng', '老朝奉'), ('XuYuan', '许愿'), ('Kana Kinoshi', '木户加奈')], max_length=31, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='color',
            field=models.CharField(choices=[('Purple', '紫'), ('White', '白'), ('Orange', '橙'), ('Blue', '蓝'), ('Red', '红'), ('Black', '黑'), ('Green', '绿'), ('Yellow', '黄')], max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='zodiac',
            name='name',
            field=models.CharField(choices=[('Pig', '猪'), ('Ox', '牛'), ('Rat', '鼠'), ('Dragon', '龙'), ('Rooster', '鸡'), ('Dog', '狗'), ('Sheep', '羊'), ('Monkey', '猴'), ('Tiger', '虎'), ('Horse', '马'), ('Snake', '蛇'), ('Rabbit', '兔')], max_length=31),
        ),
        migrations.AlterField(
            model_name='zodiacimage',
            name='name',
            field=models.CharField(choices=[('Pig', '猪'), ('Ox', '牛'), ('Rat', '鼠'), ('Dragon', '龙'), ('Rooster', '鸡'), ('Dog', '狗'), ('Sheep', '羊'), ('Monkey', '猴'), ('Tiger', '虎'), ('Horse', '马'), ('Snake', '蛇'), ('Rabbit', '兔')], max_length=31, unique=True),
        ),
    ]

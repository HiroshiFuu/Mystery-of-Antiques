# Generated by Django 2.1.4 on 2018-12-17 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoA', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='room_id',
            field=models.PositiveSmallIntegerField(help_text='Room Number', unique=True, verbose_name='Room ID'),
        ),
        migrations.AlterField(
            model_name='game',
            name='stage',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Stage'),
        ),
        migrations.AlterField(
            model_name='player',
            name='player_code',
            field=models.PositiveSmallIntegerField(help_text='Player Code', unique=True, verbose_name='Player Code'),
        ),
    ]
from django.contrib import admin

from .models import Game, Player, Character

# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = [
		'room_id',
		'stage',
	]
	filter_horizontal = ('characters',)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'color',
		'player_code',
		'game',
		'modified_at',
		'is_alive',
	]


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'skill_description',
	]
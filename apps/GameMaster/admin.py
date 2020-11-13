from django.contrib import admin

from .models import Character, Game, ZodiacImage, Zodiac, Player, PlayerAction

# Register your models here.
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'skill_description',
	]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = [
		'room_id',
		'stage',
		'created_at',
	]
	filter_horizontal = ('characters',)


@admin.register(ZodiacImage)
class ZodiacImageAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'image_tag',
	]


@admin.register(Zodiac)
class ZodiacAdmin(admin.ModelAdmin):
	list_display = [
		'pk',
		'game',
		'name',
		'genuine',
		'sequence',
		'status',
	]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'color',
		'player_code',
		'sequence',
		'step',
		'game',
		'character',
		'modified_at',
		'is_alive',
	]


@admin.register(PlayerAction)
class PlayerActionAdmin(admin.ModelAdmin):
	list_display = [
		'skill_used',
		'character',
		'player',
		'game',
		'created_at',
	]

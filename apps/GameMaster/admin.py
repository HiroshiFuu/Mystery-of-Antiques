from django.contrib import admin

from .models import Game, ZodiacImage, Zodiac, Character, Player, PlayerAction

# Register your models here.
class PlayerInline(admin.StackedInline):
    model = Player
    extra = 0


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'room_id',
        'stage',
        'created_at',
    ]
    inlines = [
        PlayerInline
    ]


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


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'skill_description',
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

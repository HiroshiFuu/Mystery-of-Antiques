from rest_framework import serializers
from apps.MoA.models import Game, ZodiacImage, Zodiac, Character, Player


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'id',
            'room_id',
            'stage',
            'created_at'
            )
        filter_horizontal = ('characters',)
        read_only_fields = ('id',)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'name',
            'color',
            'player_code',
            'sequence',
            'step',
            'game',
            'character',
            'modified_at',
            'is_alive',
        )


# class PlayerActionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PlayerAction
#       fields = (
#           'skill_used',
#           'character',
#           'player',
#           'game',
#           'created_at',
#       )


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = (
            'name',
            'skill_description',
        )


class ZodiacImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZodiacImage
        fields = (
            'name',
            'image_tag',
        )


class ZodiacSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zodiac
        fields = (
            'game',
            'name',
            'genuine',
            'sequence',
            'status',
        )
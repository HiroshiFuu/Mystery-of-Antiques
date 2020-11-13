from django.shortcuts import render
from django.core import serializers
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions

from .serializers import GameSerializer, PlayerSerializer, CharacterSerializer

from .models import Game, ZodiacImage, Zodiac, Character, Player
from .constants import CHARACTOR_CHOICES, COLOR_CHOICES, ZODIAC_CHOICES

from datetime import timedelta
import random
import json


def get_a_character(game):
    characters = game.characters.all()
    character = random.choice(characters)
    # character = characters.first()  # for testing
    game.characters.remove(character)
    return character


def get_all_colors():
    all_colors = sorted([color[0] for color in COLOR_CHOICES])
    # print(all_colors)
    return all_colors


# Create your views here.
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


@permission_classes((permissions.AllowAny,))
class CreateGame(APIView):
    def get(self, request, pk=None):
        room_id = random.randint(10000, 32767)
        while Game.objects.filter(room_id=room_id).count() > 0:
            room_id = random.randint(10000, 32767)
        request.session['room_id'] = room_id
        new_game = Game(room_id=room_id, start_color_index=random.randint(0, 7))
        new_game.save()
        zodiac_names = [zodiac[0] for zodiac in ZODIAC_CHOICES]
        # zodiac_genuines = [True] * 6 + [False] * 6
        for i in range(4):
            if i % 4 == 0:
                zodiac_genuines = [True] * 2 + [False] * 2
            name = random.choice(zodiac_names)
            zodiac_image = ZodiacImage.objects.get(name=name)
            genuine = random.choice(zodiac_genuines)
            zodiac = Zodiac(name=name, genuine=genuine, sequence=i, zodiac_image=zodiac_image, game=new_game)
            zodiac.save()
            print(zodiac)
            new_game.zodiacs.add(zodiac)
            zodiac_names.remove(name)
            zodiac_genuines.remove(genuine)
        characters = Character.objects.all()
        for character in characters:
            new_game.characters.add(character)
        # serializer = CharacterSerializer(new_game.characters.all(), many=True)
        serializer = GameSerializer(new_game)
        return Response(data=serializer.data, status=status.HTTP_200_OK, content_type='application/json')


@permission_classes((permissions.AllowAny,))
class SetupGame(APIView):
    lookup_field = 'room_id'

    def get(self, request, pk=None, room_id=None, player_code=None):
        print('SetupGame', self.kwargs, self.lookup_field)
        print('player_code', player_code)
        room_id = self.kwargs.get(self.lookup_field, None)
        if room_id is None or len(room_id) != 5:
            return Response(data={'error': 'Room ID invalid'}, status=status.HTTP_200_OK, content_type='application/json')
        game = Game.objects.filter(room_id=room_id).first()
        if game is None:
            return Response(data={'error': 'No room found'}, status=status.HTTP_200_OK, content_type='application/json')

        sesson_room_id = request.session.get('room_id', None)
        if sesson_room_id != room_id:
            request.session['room_id'] = room_id

        all_colors = get_all_colors()
        if player_code is None:
            player_code = random.randint(100, 99999)
            while Player.objects.filter(player_code=player_code).count() > 0:
                player_code = random.randint(100, 99999)
            request.session['player_code'] = player_code
            request.session['join_at'] = str(timezone.now())
            character = get_a_character(game)
            players = game.players.all()
            player_colors = [player.color for player in players]
            available_colors = [c for c in player_colors + all_colors if c not in player_colors or c not in all_colors]
            color = random.choice(available_colors)
            # color = available_colors[0] # for testing
            new_player = Player(player_code=player_code, color=color, game=game, character=character)
            name = new_player.get_color_display()
            new_player.name = name
            new_player.save()
            game.players.add(new_player)
        player = Player.objects.get(player_code=player_code)
        serializer_player = PlayerSerializer(player)
        serializer_character = CharacterSerializer(player.character)
        return Response(data={'room_id': room_id, 'player': serializer_player.data, 'character': serializer_character.data, 'colors': all_colors}, status=status.HTTP_200_OK, content_type='application/json')


@permission_classes((permissions.AllowAny,))
class TestLoadZodiacs(APIView):
    def get(self, request, pk=None, room_id=None, player_code=None):
        print('TestLoadZodics', room_id, player_code)
        if room_id is None or player_code is None:
            return Response(data={'error': 'room_id is None or player_code is None'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        game = Game.objects.get(room_id=room_id)
        if game is None:
            return Response(data={'error': 'no such Game'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        player = Player.objects.get(player_code=player_code)
        if player is None:
            return Response(data={'error': 'Player does not exist'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        stage_round = int(game.stage / 100)
        stage_round = 1
        start = stage_round - 1
        end = stage_round * 4
        # print(start, end)
        zodiacs = game.zodiacs.all()[start:end]
        ZODIACS = []
        for zodiac in zodiacs:
            ZODIACS.append({'pk': zodiac.pk, 'name': zodiac.name, 'zodiac_image_url': zodiac.zodiac_image.image.url})
        print(ZODIACS)
        return Response(data={'zodiacs': ZODIACS}, status=status.HTTP_201_CREATED, content_type='application/json')


@permission_classes((permissions.AllowAny,))
class InspectZodiac(APIView):
    def get(self, request, pk=None):
        print('InspectZodiac', pk)
        if pk is None:
            return Response(data={'error': 'pk is None'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        zodiac = Zodiac.objects.get(pk=pk)
        if zodiac is None:
            return Response(data={'error': 'no such Zodiac'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        print(zodiac)
        return Response(data={'genuine': zodiac.genuine}, status=status.HTTP_200_OK, content_type='application/json')
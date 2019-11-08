from django.shortcuts import render
from django.core import serializers
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions

from .serializers import GameSerializer, CharacterSerializer

from apps.MoA.models import Game, ZodiacImage, Zodiac, Character, Player
from apps.MoA.base_model import CHARACTOR_CHOICES, COLOR_CHOICES, ZODIAC_CHOICES

from datetime import timedelta
import random
import json


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
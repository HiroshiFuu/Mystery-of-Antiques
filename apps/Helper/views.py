from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.core import serializers

from apps.GameMaster.models import Game, ZodiacImage, Zodiac, Character, Player
from apps.GameMaster.constants import CHARACTOR_CHOICES, COLOR_CHOICES, ZODIAC_CHOICES

from datetime import timedelta
import random
import json

# Create your views here.
def Home(request):
	return render(request, 'home.html', {})


def CreateGame(request):
	print('CreateGame')
	room_id = random.randint(10000, 32767)
	while Game.objects.filter(room_id=room_id).count() > 0:
		room_id = random.randint(10000, 32767)
	new_game = Game(room_id=room_id, start_color_index=random.randint(0, 7))
	print('new_game', new_game)
	new_game.save()
	zodiac_names = [zodiac[0] for zodiac in ZODIAC_CHOICES]
	for i in range(12):
		if i % 4 == 0:
			zodiac_genuines = [True] * 2 + [False] * 2
			print()
		name = random.choice(zodiac_names)
		zodiac_image = ZodiacImage.objects.get(name=name)
		genuine = random.choice(zodiac_genuines)
		zodiac = Zodiac(name=name, genuine=genuine, sequence=i, zodiac_image=zodiac_image, game=new_game)
		zodiac.save()
		print(zodiac)
		new_game.zodiacs.add(zodiac)
		zodiac_names.remove(name)
		zodiac_genuines.remove(genuine)
	request.session['create_at'] = str(timezone.now())
	characters = Character.objects.all()
	for character in characters:
		new_game.characters.add(character)
	return render(request, 'to_setup.html', {'room_id': room_id})

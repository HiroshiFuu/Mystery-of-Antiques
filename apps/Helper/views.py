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
def home(request):
	return render(request, 'home.html', {})


def create_game(request):
	print('create_game')
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
	return render(request, 'to_setup.html', {'room_id': room_id})


def setup_game(request, room_id):
	# room_id = request.POST.get('room_id', None)
	if room_id is None or len(str(room_id)) != 5:
		return redirect('Helper:home')
	game = Game.objects.filter(room_id=room_id).first()
	if game is None:
		return redirect('Helper:home')
	# print('setup_game')
	characters = []
	for character in CHARACTOR_CHOICES:
		characters.append({'value': character[0], 'name': character[1]})
	return render(request, 'setup.html', {'room_id': room_id, 'numbers_of_players': range(1, 9), 'characters': characters})


def complete_setup_game(request, room_id):
	# room_id = request.POST.get('room_id', None)
	if room_id is None or len(str(room_id)) != 5:
		return redirect('Helper:home')
	game = Game.objects.filter(room_id=room_id).first()
	if game is None:
		return redirect('Helper:home')
	print('complete_setup_game')
	players = []
	game.players.all().delete()
	for i in range(1, 9):
		player_name = request.POST.get('player_name' + str(i), None)
		character_name = request.POST.get('character_name' + str(i), None)
		player_code = random.randint(100, 999)
		while Player.objects.filter(player_code=player_code).count() > 0:
			player_code = random.randint(100, 999)
		character = Character.objects.get(name=character_name)
		player, created = Player.objects.get_or_create(name=player_name, player_code=player_code, character=character, game=game)
		players.append({'player_name': player_name, 'character_name': character_name, 'player': player})
		game.players.add(player)
	print(players)
	print(game)
	return render(request, 'to_game.html', {'room_id': room_id})


def game(request):
	room_id = request.POST.get('room_id', None)
	if room_id is None:
		return redirect('Helper:home')

	game = Game.objects.get(room_id=room_id)
	if game.stage == -1:
		# game.stage = 0
		# To-Do: another ready check to set to 1
		game.stage = 101
		# game.save()
		# all_colors = get_all_colors()
		# start_color = all_colors[game.start_color_index]
		# player = game.players.filter(color=color).first()
		player = game.players.all().first() # for testing
		# player.sequence = 1
		# player.save()
	player_code = request.session.get('player_code', None)
	me = Player.objects.get(player_code=player_code)
	players = game.players.all()
	return HttpResponse(players)
	# return render(request, 'game.html', {'game': game, 'me': me, 'room_id': room_id, 'players': players})


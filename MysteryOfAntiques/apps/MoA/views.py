from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone

from .models import Game, ZodiacImage, Zodiac, Character, Player
from .base_model import CHARACTOR_CHOICES, COLOR_CHOICES, ZODIAC_CHOICES

from datetime import timedelta
import random
import json


def get_a_character(game):
	characters = game.characters.all()
	# character = random.choice(characters)
	character = characters.first()
	game.characters.remove(character)
	return character


def get_all_colors():
	all_colors = sorted([color[0] for color in COLOR_CHOICES])
	print(all_colors)
	return all_colors


# Create your views here.
def Home(request):
	return render(request, 'home.html', {})


def CreateGame(request):
	room_id = random.randint(10000, 32767)
	while Game.objects.filter(room_id=room_id).count() > 0:
		room_id = random.randint(10000, 32767)	
	new_game = Game(room_id=room_id, start_color_index=random.randint(0, 7))
	new_game.save()
	zodiac_names = [zodiac[0] for zodiac in ZODIAC_CHOICES]
	# zodiac_genuines = [True] * 6 + [False] * 6
	for i in range(12):
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
	request.session['create_at'] = str(timezone.now())
	characters = Character.objects.all()
	for character in characters:
		new_game.characters.add(character)
	return render(request, 'to_setup.html', {'room_id': room_id})


def RecoverPlayer(request):
	player_code = request.POST.get('player_code', None)
	if player_code is None or len(player_code) != 3:
		return redirect('MoA:Home')
	player = Player.objects.filter(player_code=player_code).first()
	if player is None:
		return redirect('MoA:Home')
	request.session['player_code'] = player_code
	room_id = player.game.room_id
	return render(request, 'to_setup.html', {'room_id': room_id})


def SetupGame(request):
	room_id = request.POST.get('room_id', None)
	if room_id is None or len(room_id) != 5:
		return redirect('MoA:Home')
	player_code = request.session.get('player_code', None)
	print(player_code)
	game = Game.objects.filter(room_id=room_id).first()
	if game is None:
		return redirect('MoA:Home')
	all_colors = get_all_colors()
	if player_code is None:
		player_code = random.randint(100, 999)
		while Player.objects.filter(player_code=player_code).count() > 0:
			player_code = random.randint(100, 999)
		request.session['player_code'] = player_code
		request.session['join_at'] = str(timezone.now())
		character = get_a_character(game)
		players = game.players.all()
		player_colors = [player.color for player in players]
		available_colors = [c for c in player_colors + all_colors if c not in player_colors or c not in all_colors]
		color = random.choice(available_colors)
		new_player = Player(player_code=player_code, color=color, game=game, character=character)
		name = new_player.get_color_display()
		new_player.name = name
		new_player.save()
		game.players.add(new_player)
	player = Player.objects.get(player_code=player_code)
	return render(request, 'setup.html', {'room_id': room_id, 'player': player, 'colors': all_colors})


def SetPlayerName(request):
	player_code = request.session.get('player_code', None)
	player = Player.objects.get(player_code=player_code)
	player.name = request.POST.get('name', None)
	player.save()
	return HttpResponse(name, status=201)


def GetConnectedPlayerColors(request):
	room_id = request.POST.get('room_id', None)
	game = Game.objects.get(room_id=room_id)
	players = game.players.all()
	player_colors = [player.color for player in players]
	return HttpResponse(json.dumps(player_colors), content_type="application/json", status=200)


def IamAlive(request):
	player_code = request.POST.get('player_code', None)
	player = Player.objects.get(player_code=player_code)
	player.save()
	return HttpResponse('alive', status=200)


def GetAlivePlayerColors(request):
	room_id = request.POST.get('room_id', None)
	game = Game.objects.get(room_id=room_id)
	if game.stage == -1:
		players = [player for player in game.players.all() if player.is_alive()]
	elif game.stage == 0:
		players = game.players.all()
	player_colors = [player.color for player in players]
	return HttpResponse(json.dumps(player_colors), content_type="application/json", status=200)


def ImAliveGetAlive(request):
	player_code = request.POST.get('player_code', None)
	player = Player.objects.get(player_code=player_code)
	player.save()
	room_id = request.POST.get('room_id', None)
	game = Game.objects.get(room_id=room_id)
	if game.stage == -1:
		players = [player for player in game.players.all() if player.is_alive()]
	elif game.stage == 0:
		players = game.players.all()
	player_colors = [player.color for player in players]
	return HttpResponse(json.dumps(player_colors), content_type="application/json", status=200)


def GameMoA(request):
	room_id = request.POST.get('room_id', None)
	if room_id is None:
		return redirect('MoA:SetupGame')
	game = Game.objects.get(room_id=room_id)
	if game.stage == -1:
		# game.stage = 0
		# To-Do: another ready check to set to 1
		game.stage = 1
		game.save()
		all_colors = get_all_colors()
		start_color = all_colors[game.start_color_index]
		player = game.players.filter(color=color).first()
		player.sequence = 1
		player.save()
	# color_sequence = []
	# for i in range(0, 8):
	# 	color_sequence.append((game.start_color_index + i) % 8)
	# # print(color_sequence)
	# all_colors = get_all_colors()
	# for i in range(0, 8):
	# 	color = all_colors[color_sequence[i]]
	# 	# print(color)
	# 	player = game.players.filter(color=color).first()
	# 	# print(player)
	# 	if player:
	# 		player.sequence = i + 1
	# 		player.save()
	player_code = request.session.get('player_code', None)
	me = Player.objects.get(player_code=player_code)
	return render(request, 'game.html', {'game': game, 'me': me})


def GetNextPlay(request):
	player_code = request.POST.get('player_code', None)
	room_id = request.POST.get('room_id', None)
	if player_code is None or room_id is None:
		return redirect('MoA:SetupGame')
	player = Player.objects.get(player_code=player_code)
	game = Game.objects.get(room_id=room_id)
	if player.sequence == game.stage:
		return HttpResponse('play', status=201)
	return HttpResponse('wait', status=200)


def EndGame(request):
	del request.session['player_code']
	# del request.session['join_at']
	# del request.session['create_at']
	return HttpResponse()
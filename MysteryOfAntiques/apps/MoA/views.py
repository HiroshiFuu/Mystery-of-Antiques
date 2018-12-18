from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from .models import Game, Character, Player, COLOR_CHOICES

import random
import json


def get_a_character(game):
	characters = game.characters.all()
	character = random.choice(characters)
	game.characters.remove(character)	
	return character


# Create your views here.
def Home(request):
	return render(request, 'home.html', {})


def CreateGame(request):
	room_id = random.randint(10000, 32767)
	new_game = Game(room_id=room_id)
	new_game.save()
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
	all_colors = [color[0] for color in COLOR_CHOICES]
	if player_code is None:
		player_code = random.randint(100, 999)
		while Player.objects.filter(player_code=player_code).count() > 0:
			player_code = random.randint(100, 999)
		request.session['player_code'] = player_code
		character = get_a_character(game)
		players = game.players.all()
		player_colors = [player.color for player in players]
		available_colors = [c for c in player_colors + all_colors if c not in player_colors or c not in all_colors]
		color = random.choice(available_colors)
		new_player = Player(player_code=player_code, color=color, game=game, character=character)
		name = new_player.get_color_display()
		new_player.name = name
		new_player.save()
	player = Player.objects.get(player_code=player_code)
	return render(request, 'setup.html', {'room_id': room_id, 'player': player, 'colors': all_colors})


def SetPlayerName(request):
	player_code = request.session.get('player_code', None)
	player = Player.objects.get(player_code=player_code)
	name = request.POST.get('name', None)
	if name is None or len(name) == 0:
		name = random.choice(names)
	player.name = name
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
	players = [player for player in game.players.all() if player.is_alive()]
	player_colors = [player.color for player in players]
	return HttpResponse(json.dumps(player_colors), content_type="application/json", status=200)


def GameMoA(request):
	return HttpResponse()


def EndGame(request):
	del request.session['player_code']
	return HttpResponse()
# -*- encoding: utf-8 -*-

from django.urls import path, re_path

from . import views

app_name = 'Helper'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create_game/', views.create_game, name='create_game'),
    path('setup_game/<int:room_id>/', views.setup_game, name='setup_game'),
    path('complete_setup_game/<int:room_id>/', views.complete_setup_game, name='complete_setup_game'),
    path('game/<int:room_id>/', views.game, name='game'),
]
from django.conf.urls import url

from . import views

app_name = 'MysterOfAntiques'

urlpatterns = [
    url(r'^Home/$', views.Home, name='Home'),
    url(r'^CreateGame/$', views.CreateGame, name='CreateGame'),
    url(r'^RecoverPlayer/$', views.RecoverPlayer, name='RecoverPlayer'),
    url(r'^SetupGame/$', views.SetupGame, name='SetupGame'),
    url(r'^SetPlayerName/$', views.SetPlayerName, name='SetPlayerName'),
    url(r'^GetConnectedPlayerColors/$', views.GetConnectedPlayerColors, name='GetConnectedPlayerColors'),
    url(r'^IamAlive/$', views.IamAlive, name='IamAlive'),
    url(r'^GetAlivePlayerColors/$', views.GetAlivePlayerColors, name='GetAlivePlayerColors'),
    url(r'^ImAliveGetAlive/$', views.ImAliveGetAlive, name='ImAliveGetAlive'),
    url(r'^GameMoA/$', views.GameMoA, name='GameMoA'),
    url(r'^GetNextPlay/$', views.GetNextPlay, name='GetNextPlay'),
    url(r'^SetNextPlayer/$', views.SetNextPlayer, name='SetNextPlayer'),
    url(r'^CheckGenuine/$', views.CheckGenuine, name='CheckGenuine'),
    url(r'^StartBB/$', views.StartBB, name='StartBB'),
    url(r'^EndGame/$', views.EndGame, name='EndGame'),
    url(r'^TestGameMoA/$', views.TestGameMoA, name='TestGameMoA'),
]
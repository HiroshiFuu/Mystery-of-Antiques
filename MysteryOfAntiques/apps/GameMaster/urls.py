from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

from .views import GameViewSet, CreateGame, SetupGame
from .views import TestLoadZodics

app_name = 'MysterOfAntiques'

schema_view = get_swagger_view(title='MofA API')

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'Game', GameViewSet)

urlpatterns = [
    url(r'^$', schema_view),
    url(r'^CreateGame', CreateGame.as_view()),
    url(r'^SetupGame/(?P<room_id>\d+)/$', SetupGame.as_view()),
    url(r'^SetupGame/(?P<room_id>\d+)/(?P<player_code>\d+)/$', SetupGame.as_view()),
    url(r'^TestLoadZodics/(?P<room_id>\d+)/(?P<player_code>\d+)/$', TestLoadZodics.as_view()),
]
urlpatterns += router.urls
from django.conf.urls import url

from . import views

app_name = 'Helper'

urlpatterns = [
    url(r'^Home/$', views.Home, name='Home'),
    url(r'^CreateGame/$', views.CreateGame, name='CreateGame'),
]
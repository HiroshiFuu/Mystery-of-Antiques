# -*- coding:utf-8 -*-
from django import http
from django.urls import reverse


def index(request):
	return http.HttpResponseRedirect(reverse('Helper:home'))
	if request.user.is_authenticated:
		# url = reverse('users:detail', kwargs={'username': request.user.username})
		return http.HttpResponseRedirect(reverse('Helper:home'))
	else:
		return http.HttpResponseRedirect(reverse('account_login'))

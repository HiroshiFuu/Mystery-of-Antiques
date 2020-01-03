# -*- coding:utf-8 -*-
__author__ = 'Michal Kulaczkowski'
import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)

from threading import local

# thread local support
_thread_locals = local()


def set_current_user(user):
    """
    Assigns current user from request to thread_locals, used by
    CurrentUserMiddleware.
    """
    _thread_locals.user = user


def get_current_user():
    """
    Returns current user, or None
    """
    user = getattr(_thread_locals, 'user', None)
    if user:
        return user
    else:
        return AnonymousUser()


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Adds currently logged user information to thread
    """

    def process_request(self, request):
        set_current_user(getattr(request, 'user', None))

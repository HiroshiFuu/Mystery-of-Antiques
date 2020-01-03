"""
Local settings for Sensor Catalogue project.

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""
from .base import *  # noqa


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = ['10.228.242.53', '127.0.0.1', 'iotsite.ngrok.io']


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = 'VZ4!q(yhF+$=Xc-qE9Bh=d+FQ(n$Vqx|1Ia0DmowHHMpxV:Xt^'


# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
		'LOCATION': ''
	}
}


# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += [
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_CONFIG = {
	'DISABLE_PANELS': [
		'debug_toolbar.panels.redirects.RedirectsPanel',
	],
	'SHOW_TEMPLATE_CONTEXT': True,
}


# django-corsheaders
# ------------------------------------------------------------------------------
MIDDLEWARE += [
	'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True


# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += [
    'debug_toolbar',
    'corsheaders',
]

INTERNAL_IPS = ['127.0.0.1', ]


# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(str(ROOT_DIR), 'local_fenghao.sqlite3'),
    }
}


# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

SILENCED_SYSTEM_CHECKS = ['mysql.E001']


# local-apps
# ------------------------------------------------------------------------------
INSTALLED_APPS += [
]
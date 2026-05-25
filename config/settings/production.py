from .base import *
from decouple import config, Csv

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Говорим Django доверять заголовкам от nginx
SECURE_PROXY_SSL_HEADER    = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST       = True

# CSRF — разрешаем наш домен
CSRF_TRUSTED_ORIGINS = [
    'http://3dom.space',
    'http://www.3dom.space',
    'https://3dom.space',
    'https://www.3dom.space',
]

# Куки безопасности — включаем только после настройки SSL
SESSION_COOKIE_SECURE      = False
CSRF_COOKIE_SECURE         = False
SECURE_HSTS_SECONDS        = 0

STATIC_ROOT = '/app/staticfiles'
MEDIA_ROOT  = '/app/media'

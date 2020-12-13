DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = 'qVUeDB48y3gGXUMtcuaDcFHNzoGeXXoiIpUwOcaE'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: DEBUG,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'mdillon__postgis',
    }
}

REDIS_HOST = 'redis'
REDIS_PORT = 6379

CONSTANCE_REDIS_PREFIX = 'constance:gecolsa:'
CONSTANCE_REDIS_CONNECTION = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': 0,
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            f'{REDIS_HOST}:{REDIS_PORT}'
        ],
        'OPTIONS': {
            'DB': 1,
        }
    },
    'sessions': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            f'{REDIS_HOST}:{REDIS_PORT}'
        ],
        'OPTIONS': {
            'DB': 2,
        }
    },
}

CELERY_ALWAYS_EAGER = False
BROKER_URL = 'redis://{0}:{1}/{2}'.format(REDIS_HOST, REDIS_PORT, 3)

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_USE_SSL = True

GOOGLE_TAG_MANAGER_SCRIPT = ''
GOOGLE_TAG_MANAGER_IFRAME = ''

# RAVEN_CONFIG = {
#     'dsn': '',
# }

EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

PAGOS_ON_LINE = {
    'prueba': True,
    'usuarioId': '',
    'llaveEncripcion': '',
    'url': 'https://gateway.pagosonline.net/apps/gateway/index.html',
    'test_url': 'https://gateway2.pagosonline.net/apps/gateway/index.html',
}

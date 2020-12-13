DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'testdb',
        'USER': 'postgres',
        'HOST': 'mdillon__postgis',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.backends.dummy.RedisDummyCache',
    },
    'sessions': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

SECRET_KEY = 'test'

USE_TZ = False

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'
    },
}

CELERY_ALWAYS_EAGER = True
BROKER_URL = ''

COMPRESS_ENABLED = False

CONSTANCE_REDIS_CONNECTION_CLASS = 'app.redis_mockup.Connection'
CONSTANCE_REDIS_CONNECTION = {}

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_USE_SSL = False

GOOGLE_TAG_MANAGER_SCRIPT = ''
GOOGLE_TAG_MANAGER_IFRAME = ''

PAGOS_ON_LINE = {
    'prueba': True,
    'usuarioId': '',
    'llaveEncripcion': '',
    'url': 'https://gateway.pagosonline.net/apps/gateway/index.html',
    'test_url': 'https://gateway2.pagosonline.net/apps/gateway/index.html',
}


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

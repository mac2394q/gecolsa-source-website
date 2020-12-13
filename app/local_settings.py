DEBUG = False

ALLOWED_HOSTS = ['gecolsa.com']

SECRET_KEY = '8228J48CUKqsaitnKBR6sSpTPv0Re6H9X9ca4pBKanZaerYSaOBBkYJKymEW7X+R'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: DEBUG,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gecolsa',
        'USER': 'deploy',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

CONSTANCE_REDIS_PREFIX = 'constance:gecolsa:'
CONSTANCE_REDIS_CONNECTION = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': 0,
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{0}:{1}/{2}'.format(REDIS_HOST, REDIS_PORT, 1),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'sessions': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{0}:{1}/{2}'.format(REDIS_HOST, REDIS_PORT, 2),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

CELERY_ALWAYS_EAGER = False
BROKER_URL = 'redis://{0}:{1}/{2}'.format(REDIS_HOST, REDIS_PORT, 3)

RECAPTCHA_PUBLIC_KEY = '6Leh_RgTAAAAAGGjTBNKoZnA31NgwfQjoC8DfY07'
RECAPTCHA_PRIVATE_KEY = '6Leh_RgTAAAAAG0bqKYRMl5Xp0n_iaMQdiB7uKif'
RECAPTCHA_USE_SSL = True

FILE_UPLOAD_PERMISSIONS = 0o644

GOOGLE_TAG_MANAGER_SCRIPT = '''
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-NWRMCPL');</script>
'''
GOOGLE_TAG_MANAGER_IFRAME = '''
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NWRMCPL"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
'''

RAVEN_CONFIG = {
    'dsn': 'https://db47cb885fd140fdb02b01768e1dceae:270462644d064d249bd9bb52986aada5@sentry.axiacore.com/65',
}

EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAZVMAEXG7TZMNUVNO'
EMAIL_HOST_PASSWORD = 'BJSZ7s5w4LtVN2lFU1sFHcV8aKPf7MPNjRvPaYgsFJX5'

PAGOS_ON_LINE = {
    'prueba': False,
    'usuarioId': '109322',
    'llaveEncripcion': '14abfc045c2',
    'url': 'https://gateway.pagosonline.net/apps/gateway/index.html',
    'test_url': 'https://gateway2.pagosonline.net/apps/gateway/index.html',
}

DEFAULT_EMAIL_COMPLAINT = ['denunciaslineaetica@soe360grados.com.co']

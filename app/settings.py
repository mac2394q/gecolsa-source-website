import os
import sys
import djcelery
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_APPS = (
    'app',
    'cms',
    'common',
    'shop',
    'product',
    'userprofile',
)

INSTALLED_APPS = PROJECT_APPS + (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    'axes',
    'captcha',
    'celery_haystack',
    'compressor',
    'constance',
    'crispy_forms',
    'debug_toolbar',
    'django_extensions',
    'djcelery',
    'haystack',
    'markdown_deux',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'sorl.thumbnail',
    'widget_tweaks',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.google_tag_manager_script',
                'app.context_processors.google_tag_manager_iframe',
                'constance.context_processors.config',
                'common.context_processors.alliances',
                'common.context_processors.site_processor',
            ],
        },
    },
]

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

# django-debug-toolbar
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

FOOTER_CACHE_TIME = 60 * 60 * 24  # cache footer for one day (in seconds)

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = False

USE_TZ = True

SITE_ID = 1

AUTH_USER_MODEL = 'userprofile.User'

LOGIN_URL = 'userprofile:login'

LOGIN_REDIRECT_URL = 'userprofile:my_gecolsa'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

STATIC_URL = '/static/'

MEDIA_URL = '/uploads/'

PHONE_NUMBER_LENGTH = 7

# Caterpillar WSDL see: http://goo.gl/qB5QoH
CATERPIRLLAR_WSDL = 'https://cpc.cat.com/ws/services/XmlUpdate?wsdl'
CATERPIRLLAR_SCC = 'R460'

# Shop integration
SHOP_RATING_ENDPOINT = \
    'http://190.144.216.154:89/wsSOE360OnlineStore/rest/jsonServices/shipping'
SHOP_SELL_ENDPOINT = \
    'http://190.144.216.154:89/wsSOE360OnlineStore/rest/jsonServices/order'
SHOP_PRODUCT_ENDPOINT = \
    'http://190.144.216.154:89/wsSOE360OnlineStore/rest/jsonServices/inventory'

# See main classes
# http://cat-ebusiness.com/cpc/developers/nightly-batch-process/
CATERPILLAR_CLASSES = ['405', '406', '486', '402']

# django-constance
CONSTANCE_CONFIG = {
    'CHAT_URL': (
        'http://190.143.102.170/epro/Chat/CPChatRequest.htm',
        'URL del servicio de chat'
    ),
    'EMAIL_TO_CONTACT': (
        'mac2394q@gmail.com',
        '''Correo electrónico al que se envía el contacto, en la página de
        contacto solo será visible el primero.'''
    ),
    'TAX_VALUE': (
        0.16,
        'Valor predeterminado del impuesto en caso de falla de webservice'
    ),
    'SHIPPING_VALUE': (
        20000,
        'Valor predeterminado del envío en caso de falla de webservice',
    ),
    'EMAIL_GECOLSA_WSDL': (
        'luz.vanegas@soe360grados.com.co, anamaria_nunez@gecolsa.com.co ',
        '''Correos separados por coma para reportar problema al consumir
        webservice''',
    ),
    'EMAIL_GECOLSA_PRODUCTS': (
        'luz.vanegas@soe360grados.com.co, david.canon@soe360grados.com.co',
        'Correos separados por coma para reportar compra de merchandise',
    ),
    'EMAIL_GECOLSA_ADMIN': (
        'anamaria_nunez@gecolsa.com.co, andres_paez@gecolsa.com.co',
        '''Correos separados por coma para reportar a administrador de
        plataforma''',
    ),
    'EMAIL_GECOLSA_LEGAL': (
        'anamaria_nunez@gecolsa.com.co, luz.vanegas@soe360grados.com.co',
        '''Correo que se ofrece a los usuarios que se inscriben''',
    ),
    'EMAIL_SATELITAL': (
        'luz.vanegas@soe360grados.com.co, anamaria_nunez@gecolsa.com.co',
        '''Correo que recibe información de las solicitudes satelitales''',
    ),
    'PRODUCT_LINE_PDF': (
        'http://cl.ly/0X3h1S3g1k41/download/linea_producto_final_0.pdf',
        '''URL de la línea de producto''',
    ),
    'PHONE_CONTACT': (
        '01 8000 919 920',
        '''Número telefónico de contacto''',
    ),
    'WHATSAPP_CONTACT': (
        '318 242 2091',
        '''Número de contacto whatsapp''',
    ),
    'WEBSERVICE_KEY': (
        'SC4QP-KAQGR58-FHWWVGQYC97E',
        '''Llave para consumir el servicio de actualización de inventario,
        recomendado caracteres alfanuméricos.  Cámbiela regularmente para
        garantizar seguridad del sistema.''',
    ),
    'STORE_IS_OPEN': (
        True,
        '''Indica si la tienda está abierta para que aparezca en los menús
        '''
    )
}

# django-crispy
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# sorl-thumbnail
THUMBNAIL_DEBUG = False
THUMBNAIL_FORMAT = 'PNG'

# Email settings
DEFAULT_FROM_EMAIL = 'asalguero@questips.com'
DEFAULT_TO_EMAIL = ['atencionalcliente@gecolsa.com.co']
DEFAULT_EMAIL_COMPLAINT = ['denunciaslineaetica@soe360grados.com.co']

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'sessions'

# django-axes
AXES_LOGIN_FAILURE_LIMIT = 3
AXES_USE_USER_AGENT = True
AXES_COOLOFF_TIME = 24
AXES_LOCKOUT_TEMPLATE = '429.html'

# django-compressor
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]

# Django celery
djcelery.setup_loader()

CELERY_TASK_RESULT_EXPIRES = 86400 * 90  # keep task results for 90 days
CELERY_DISABLE_RATE_LIMITS = True
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_SCHEDULE = {
    'Update CAT products daily at 12:05': {
        'task': 'product.tasks.task_update_products',
        'schedule': crontab(hour=5, minute=0),
    },
    'Rebuild Index every hour': {
        'task': 'app.tasks.task_update_index',
        'schedule': crontab(minute='*/15'),
    },
    'Get information from new products daily at 6:30': {
        'task': 'shop.tasks.task_fetch_products',
        'schedule': crontab(hour=6, minute=30),
    },
}

# Haystack Config
SEARCH_IDX_UPDATE_FREQUENCY = 2
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index')
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'

# pylint: disable=wrong-import-position,unused-wildcard-import,wildcard-import
if 'test' in sys.argv:
    from app.test_settings import *

    from unittest.mock import patch
    patch('os.path.getsize', return_value=10).start()

else:
    from app.local_settings import *     # pylint: disable=E0611,E0401

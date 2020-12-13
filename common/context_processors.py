from django.conf import settings
from django.core.cache import cache
from django.contrib.sites.models import Site

from common.models import Alliance


def alliances(request):
    alliance = cache.get('ALLIANCES')
    if not alliance:
        alliance = {
            'ALLIANCES': Alliance.objects.filter(is_active=True),
        }
        cache.set(
            'ALLIANCES',
            alliance,
            settings.FOOTER_CACHE_TIME,
        )

    return alliance


def site_processor(request):
    """Make the current site available from the templates
    """
    return {
        'current_site': Site.objects.get_current()
    }

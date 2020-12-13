from django.conf import settings
from django.utils.safestring import mark_safe


def google_tag_manager_script(request):
    return {'GOOGLE_TAG_MANAGER_SCRIPT': mark_safe(
        settings.GOOGLE_TAG_MANAGER_SCRIPT
    )}


def google_tag_manager_iframe(request):
    return {'GOOGLE_TAG_MANAGER_IFRAME': mark_safe(
        settings.GOOGLE_TAG_MANAGER_IFRAME
    )}

from django.contrib import admin

from . import models


class RedactorModelAdmin(admin.ModelAdmin):
    """Integrate redactor to the admin site.
    """
    class Media:
        css = {
            'all': (
                'vendor/redactor/redactor.css',
                'css/admin/django-redactor.css',
            )
        }
        js = (        # pylint: disable=C0103
            '//ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js',
            'vendor/redactor/redactor.min.js',
            'vendor/redactor/plugins/table.js',
            'js/admin-redactor.js',
        )

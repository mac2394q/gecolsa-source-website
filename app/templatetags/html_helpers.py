# pylint: disable=C0103
import unicodedata

from django import template
from django.utils.html import strip_tags

register = template.Library()


def html_extract_text(html_text):
    """Used for index html text documents
    removes all HTML tags from the document, replacing them with spaces.

    Does almost the same thing that

    https://docs.djangoproject.com/en/dev/ref
    /utils/#django.utils.html.strip_tags

    but it doesn't get the words stuck together and replaces accents.
    """
    return ' '.join([word[:240] for word in strip_tags(html_text).split()])

register.filter('html_extract_text', html_extract_text)


def strip_accents(my_string):
    return ''.join((
        mch for mch in unicodedata.normalize('NFD', '{0}'.format(my_string))
        if unicodedata.category(mch) != 'Mn'
    ))


def unaccent(text):
    return strip_accents(text)

register.filter('unaccent', unaccent)

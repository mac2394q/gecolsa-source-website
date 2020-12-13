from django import template
from django.urls import reverse
from django.db.models import Count

from cms.models import Page
from cms.models import CommunicationCategory
from shop.models import ProductCategory


register = template.Library()


@register.inclusion_tag('cms/_accordion.html')
def get_accordion(page):
    first_level_parent = page.get_parents[0]
    return {
        'page': page,
        'second_level_pages': Page.objects.filter(
            parent=first_level_parent,
            is_active=True,
        ),
    }


@register.inclusion_tag('layout/_menu_item.html')
def get_menu_item(page_slug):
    page = Page.objects.get(slug=page_slug)
    return {
        'item': page,
        'show_third_level': False,
    }


@register.inclusion_tag('layout/_menu_link.html')
def get_menu_link(page_slug):
    page = Page.objects.get(slug=page_slug)
    return {
        'item': page,
    }


@register.inclusion_tag('layout/_footer_item.html')
def get_footer_item(page_slug):
    page = Page.objects.get(slug=page_slug)
    return {
        'item': page,
    }


@register.inclusion_tag('layout/_footer_item.html')
def get_footer_communication(title):
    return {
        'item': {
            'get_absolute_url': reverse(
                'cms:communication_list',
            ),
            'title': title,
            'children': CommunicationCategory.objects.all().order_by(
                'position'
            ),
        },
    }


@register.inclusion_tag('layout/_footer_item.html')
def get_merchandising_item():
    """ Merchandising categories.
    """
    return {
        'item': {
            'get_absolute_url': reverse(
                'shop:home',
            ),
            'title': 'MERCHANDISING',
            'children': ProductCategory.objects.filter(
                is_active=True
            ).annotate(
                product_count=Count('products')
            ).filter(product_count__gt=0),
        },
    }

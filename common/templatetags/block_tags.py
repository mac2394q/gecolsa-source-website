from django import template
from django.core.cache import cache

from common.models import FixedBlock
from common.models import ImageLink
from cms.models import CommunicationCategory
from cms.models import Communication
from cms.models import Page


register = template.Library()


@register.inclusion_tag('common/image_link_list.html')
def get_link_list(section):
    """Adds a block with linked images
    """
    if isinstance(section, str):
        return {
            'link_list': ImageLink.objects.filter(section=section)[:3],
        }
    if (
        isinstance(section, Page) or
        isinstance(section, Communication) or
        isinstance(section, CommunicationCategory)
    ):
        link_list = [
            {
                'title': section.footer_title_1,
                'url': section.footer_link_1,
                'image': section.footer_image_1,
            }, {
                'title': section.footer_title_2,
                'url': section.footer_link_2,
                'image': section.footer_image_2,
            }, {
                'title': section.footer_title_3,
                'url': section.footer_link_3,
                'image': section.footer_image_3,
            },
        ]
        return {
            'link_list': link_list,
        }
    return {}


@register.filter
def get_fixed_block(block_slug):
    key = 'fixed-block-{0}'.format(block_slug)
    if cache.get(key, None):
        block = cache.get(key)
    else:
        block = FixedBlock.objects.get(slug=block_slug)
        cache.set(key, block, 86400)
    return block

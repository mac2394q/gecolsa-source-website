from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from cms.models import Page
from cms.models import Communication
from cms.models import CommunicationCategory
from product.models import EquipmentCategory
from product.models import EquipmentSubCategory
from product.models import Equipment
from product.models import UsedEquipment


class StaticViewSitemap(Sitemap):
    priority = 1.0

    def items(self):
        return [
            'home',
            'contact',
            'office_list',
        ]

    def location(self, item):
        return reverse(item)


class PageDetailSitemap(Sitemap):

    def items(self):
        return Page.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at


class CommunicationCategorySitemap(Sitemap):

    def items(self):
        return CommunicationCategory.objects.all()


class CommunicationDetailSitemap(Sitemap):

    def items(self):
        return Communication.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at


class EquipmentCategorySitemap(Sitemap):

    def items(self):
        return EquipmentCategory.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at


class EquipmentSubCategorySitemap(Sitemap):

    def items(self):
        return EquipmentSubCategory.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at


class EquipmentDetailSitemap(Sitemap):

    def items(self):
        return Equipment.objects.filter(
            is_active=True,
            subcategories__isnull=False,
        )

    def lastmod(self, obj):
        return obj.created_at


class UsedEquipmentDetailSitemap(Sitemap):

    def items(self):
        return UsedEquipment.objects.filter(
            is_active=True,
            categories__isnull=False,
        )

    def lastmod(self, obj):
        return obj.created_at


sitemaps = {
    'static': StaticViewSitemap,
    'page': PageDetailSitemap,
    'communication': CommunicationDetailSitemap,
    'communication_category': CommunicationCategorySitemap,
    'equipment_category': EquipmentCategorySitemap,
    'equipment_subcategory': EquipmentSubCategorySitemap,
    'equipment': EquipmentDetailSitemap,
    'used_equipment': UsedEquipmentDetailSitemap,
}

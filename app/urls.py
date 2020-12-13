from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.urls import re_path

from django.views.generic.base import TemplateView
from haystack.generic_views import SearchView

from app.views import HomeView, RedactorUploadView,CleanCacheView, RequestsComplaintsView
from app.forms import FileForm, ImageForm
from app.sitemaps import sitemaps
from shop.views import UpdateShopProducts
from shop.views import CitySearch
from common.views import ContactView
from common.views import OfficeListView
from common.views import ContactFormView
from cms.views import SatelliteMonitoringContactView
from cms.views import ReportSatelliteXls
from product.views import XmlUpdateView


urlpatterns = [
    # Home
    path('', HomeView.as_view(), name='home'),

    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt'),
    ),

    # Admin URLs
    path(
        'admin/clean_cache/',
        CleanCacheView.as_view(),
        name='clean_cache',
    ),
    path(
        'admin/cat_xml_sync/',
        XmlUpdateView.as_view(),
        name='cat_xml_sync',
    ),
    path(
        'admin/update_shop_products/',
        UpdateShopProducts.as_view(),
        name='update_shop_products',
    ),
    path(
        'admin/satellite_interest_report/',
        ReportSatelliteXls.as_view(),
        name='download_satellite_report',
    ),
    path('admin/', admin.site.urls),
    re_path(
        r'^admin/redactor/upload/image/(?P<upload_to>.*)$',
        RedactorUploadView.as_view(form_class=ImageForm),
        name='redactor_upload_image'
    ),
    re_path(
        r'^admin/redactor/upload/file/(?P<upload_to>.*)$',
        RedactorUploadView.as_view(form_class=FileForm),
        name='redactor_upload_file'
    ),

    path(
        'buscar/',
        SearchView.as_view(),
        name='search',
    ),

    path(
        'solicitudes-y-denuncias/',
        RequestsComplaintsView.as_view(),
        name='requests_complaints'
    ),

    # Monitoreo Satelital
    path(
        'monitoreo-satelital/',
        SatelliteMonitoringContactView.as_view(),
        name='satellital_tracking',
    ),

    # Sitemap
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='sitemap',
    ),

    # Contact
    path('contacto/', ContactView.as_view(), name='contact'),

    # Offices
    path('sedes/', OfficeListView.as_view(), name='office_list'),

    # shop
    path(
        'tienda/',
        include('shop.urls', namespace='shop')
    ),

    # CMS
    path(
        'maquinaria/',
        include('cms.urls', namespace='cms')
    ),

    # Products
    path(
        'equipos/',
        include('product.urls', namespace='equipment')
    ),

    # Usuarios
    path(
        'cuentas/',
        include('userprofile.urls', namespace='userprofile')
    ),

    # API City-Serch
    re_path(
        r'^city-search/(?P<query>.*)/$',
        CitySearch.as_view(), name='city-search'
    ),

    path(
        'contact_form_view/',
        ContactFormView.as_view(),
        name='contact_form',
    ),

    # API
    path(
        'api/',
        include('localapi.urls', namespace='api')
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

from django.views.generic import TemplateView
from django.urls import path

from cms.views import CommunicationListView
from cms.views import CommunicationDetailView
from cms.views import PageDetailView

app_name = 'cms'
urlpatterns = [
    path(
        'comunicacion/',
        CommunicationListView.as_view(),
        name='communication_list',
    ),

    path(
        'comunicacion/categoria/<slug:slug>/',
        CommunicationListView.as_view(),
        name='communication_by_category_list',
    ),

    path(
        'comunicacion/<slug:slug>/',
        CommunicationDetailView.as_view(),
        name='communication_detail',
    ),

    path(
        'reparacion/nivel-de-reparacion/',
        TemplateView.as_view(template_name="cms/_repair_level.html"),
        name='repair'
    ),

    path(
        '<slug:slug>/',
        PageDetailView.as_view(),
        name='page_detail',
    ),
]

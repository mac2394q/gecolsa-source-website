from django.urls import re_path

from localapi.views import UpdateInventoryView

app_name = 'localapi'
urlpatterns = [
    re_path(
        r'^update_inventory/(?P<key>[-\w]+)/$',
        UpdateInventoryView.as_view(),
        name='update_inventory',
    ),
]

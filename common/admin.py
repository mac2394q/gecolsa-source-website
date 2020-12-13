from django.contrib import admin
from common.models import SliderHome
from common.models import Alliance
from common.models import City
from common.models import CompanyType
from common.models import Contact
from common.models import Office
from common.models import FixedBlock
from common.models import ImageLink
from common.models import WsLog


@admin.register(SliderHome)
class SliderHomeAdmin(admin.ModelAdmin):
    list_display = (
        'position',
        'is_active',
        'url_text',
        'url',
    )

    fields = (
        'image_desktop',
        'image_tablet',
        'image_mobile',
        'url',
        'url_text',
        'position',
        'is_external',
        'is_active',
    )


@admin.register(Alliance)
class AllianceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'url',
        'position',
        'is_active',
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'city',
        'latlon',
        'is_active',
    )


@admin.register(FixedBlock)
class FixedBlockAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
    )

    readonly_fields = (
        'slug',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(FixedBlockAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ImageLink)
class ImageLinkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'section',
    )


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'mobile_number',
        'email',
        'contact_by',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'mobile_number',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return super(
                ContactAdmin,
                self
            ).get_readonly_fields(
                request,
                obj,
            )
        # make all fields readonly
        read_only_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return read_only_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ContactAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(WsLog)
class WsLogAdmin(admin.ModelAdmin):

    actions = None

    list_display = [
        'category',
        'status_code',
        'ellapsed_time',
        'created_at',
    ]

    list_filter = [
        'status_code',
        'category',
        'created_at',
    ]

    search_fields = [
        'request_data',
        'answer_data',
        'id',
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        read_only_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return read_only_fields

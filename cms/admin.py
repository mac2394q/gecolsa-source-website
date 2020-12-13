from django.contrib import admin
from django.utils.timezone import now

from cms.models import Page
from cms.models import Gallery
from cms.models import RelatedFile
from cms.models import RelatedLink
from cms.models import CommunicationNews
from cms.models import CommunicationEvent
from cms.models import CommunicationGallery
from cms.models import CommunicationCategory
from cms.models import CommunicationRelatedFile
from cms.models import SatelliteMonitoringContact
from cms.models import Block
from cms.models import FeaturedContent
from cms.forms import PageForm
from cms.forms import EventForm
from cms.forms import CommunicationForm
from cms.forms import CommunicationCategoryForm


from app.admin import RedactorModelAdmin


class GalleryInline(admin.TabularInline):
    model = Gallery
    sortable_field_name = 'position'


class RelatedFileInline(admin.TabularInline):
    model = RelatedFile


class RelatedLinkInline(admin.TabularInline):
    model = RelatedLink


@admin.register(Page)
class PageAdmin(RedactorModelAdmin):
    list_display = (
        'title',
        'parent',
        'position',
        'has_children_accordion',
        'show_children',
        'created_at',
        'is_active',
    )

    search_fields = (
        'title',
        'slug',
        'parent__title',
    )

    readonly_fields = [
        'updated_at',
    ]

    form = PageForm

    fieldsets = (
        (None, {
            'fields': (
                ('title', 'is_active'),
                ('parent', 'position'),
                'image',
                'list_image',
                'video_url',
            ),
        }),
        ('Resumen', {
            'fields': (
                'summary',
            ),
        }),
        ('Contenido', {
            'fields': (
                'content',
            ),
        }),
        ('Presentación del contenido en la página', {
            'fields': (
                'has_children_accordion',
                'show_children',
            ),
        }),
        ('Bloques inferiores de la página', {
            'fields': (
                ('footer_title_1', 'footer_link_1', 'footer_image_1'),
                ('footer_title_2', 'footer_link_2', 'footer_image_2'),
                ('footer_title_3', 'footer_link_3', 'footer_image_3'),
            ),
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
            ),
        }),
    )

    inlines = [
        GalleryInline,
        RelatedFileInline,
        RelatedLinkInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        model_form = super(PageAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(model_form):
            def __new__(cls, *args, **kwargs):
                kwargs['object'] = obj
                return model_form(*args, **kwargs)

        return ModelFormMetaClass

    def has_delete_permission(self, request, obj=None):
        if obj and not obj.parent:
            return False
        return True

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj and obj.parent is None:
            if 'parent' not in readonly_fields:
                readonly_fields = readonly_fields + ['parent']
            if (
                not obj.has_children_accordion and
                'has_children_accordion' not in readonly_fields
            ):
                readonly_fields = readonly_fields + ['has_children_accordion']
            if 'position' not in readonly_fields:
                readonly_fields = readonly_fields + ['position']
        return readonly_fields

    def save_model(self, request, obj, form, change):
        obj.updated_at = now()

        super(
            PageAdmin,
            self
        ).save_model(
            request,
            obj,
            form,
            change,
        )


@admin.register(CommunicationCategory)
class CommunicationCategoryAdmin(admin.ModelAdmin):
    form = CommunicationCategoryForm

    list_display = (
        'title',
        'slug',
        'position',
        'has_comments',
        'has_share_buttons',
        'created_at',
    )

    search_fields = (
        'title',
        'slug',
    )

    exclude = (
        'created_at',
    )

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'position',
                'has_comments',
                'has_share_buttons',
            ),
        }),
        ('Bloques inferiores de la página', {
            'fields': (
                ('footer_title_1', 'footer_link_1', 'footer_image_1'),
                ('footer_title_2', 'footer_link_2', 'footer_image_2'),
                ('footer_title_3', 'footer_link_3', 'footer_image_3'),
            ),
        }),
    )

    def has_delete_permission(self, request, obj=None):
        if obj and (obj.slug == 'eventos' or obj.slug == 'novedades'):
            return False
        return True

    def get_actions(self, request):
        actions = super(CommunicationCategoryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj and (obj.slug == 'eventos' or obj.slug == 'novedades'):
            readonly_fields = readonly_fields + ('title',)
        return readonly_fields


class CommunicationGalleryInline(admin.TabularInline):
    model = CommunicationGallery
    sortable_field_name = 'position'


class CommunicationRelatedFileInline(admin.TabularInline):
    model = CommunicationRelatedFile


@admin.register(CommunicationNews)
class CommunicationAdmin(RedactorModelAdmin):
    form = CommunicationForm

    inlines = [
        CommunicationGalleryInline,
        CommunicationRelatedFileInline,
    ]

    search_fields = (
        'title',
        'slug',
        'category__title',
    )

    list_display = (
        'title',
        'category',
        'is_active',
        'has_contact',
        'created_at',
    )

    exclude = (
        'created_at',
        'event_date',
        'event_hour',
        'event_place',
    )

    readonly_fields = [
        'updated_at',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'category',
                'image',
                'list_image',
                'is_active',
                'has_contact',
            ),
        }),
        ('Contenido', {
            'fields': (
                'content',
                'extended_content',
            ),
        }),
        ('Bloques inferiores de la página', {
            'fields': (
                ('footer_title_1', 'footer_link_1', 'footer_image_1'),
                ('footer_title_2', 'footer_link_2', 'footer_image_2'),
                ('footer_title_3', 'footer_link_3', 'footer_image_3'),
            ),
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.updated_at = now()

        super(
            CommunicationAdmin,
            self
        ).save_model(
            request,
            obj,
            form,
            change,
        )


@admin.register(CommunicationEvent)
class CommunicationEventAdmin(RedactorModelAdmin):
    form = EventForm

    inlines = [
        CommunicationGalleryInline,
    ]

    search_fields = (
        'title',
        'slug',
        'event_city',
        'event_place',
    )

    list_display = (
        'title',
        'event_date',
        'event_hour',
        'event_city',
        'event_place',
        'created_at',
        'is_active',
    )

    readonly_fields = [
        'updated_at',
    ]

    exclude = (
        'created_at',
        'category',
    )

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'is_active',
                'image',
                'list_image',
            ),
        }),
        ('Contenido', {
            'fields': (
                'content',
                'extended_content',
            ),
        }),
        ('Información del evento', {
            'fields': (
                ('event_date', 'event_hour', 'end_date'),
                ('event_city', 'event_place'),
            ),
        }),
        ('Bloques inferiores de la página', {
            'fields': (
                ('footer_title_1', 'footer_link_1', 'footer_image_1'),
                ('footer_title_2', 'footer_link_2', 'footer_image_2'),
                ('footer_title_3', 'footer_link_3', 'footer_image_3'),
            ),
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.category = CommunicationCategory.objects.get(slug='eventos')
        obj.updated_at = now()

        super(
            CommunicationEventAdmin,
            self
        ).save_model(
            request,
            obj,
            form,
            change,
        )


@admin.register(SatelliteMonitoringContact)
class SatelliteMonitoringContactAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'company',
        'email',
        'created_at',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(SatelliteMonitoringContactAdmin, self).get_actions(
            request
        )
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        read_only_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return read_only_fields


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):

    list_display = (
        'identifier',
        'content',
        'url',
        'is_active',
    )

    readonly_fields = ('identifier', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FeaturedContent)
class FeaturedContentAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'summary',
        'is_external',
        'url',
    )

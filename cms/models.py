from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.html import strip_tags

from autoslug import AutoSlugField

from app.utils import unique_case_insensitive


class Page(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    summary = models.TextField(
        verbose_name='resumen para el header',
    )

    image = models.ImageField(
        max_length=256,
        upload_to='cms/page/',
        verbose_name='imagen del banner principal',
        help_text='El tamano de la imágen debe ser 1920x469px',
    )

    list_image = models.ImageField(
        max_length=256,
        upload_to='cms/page-list/',
        verbose_name='imagen para listados',
        help_text='El tamano de la imágen debe ser 320x410px',
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='página padre',
        blank=True,
        null=True,
        related_name='children',
    )

    slug = AutoSlugField(
        populate_from='title',
        unique=True,
    )

    position = models.PositiveIntegerField(
        verbose_name='posición',
    )

    content = models.TextField(
        verbose_name='contenido de la página',
        blank=True,
    )

    has_children_accordion = models.BooleanField(
        verbose_name='muestra menú lateral',
        default=False,
    )

    show_children = models.BooleanField(
        verbose_name='mostrar hijos',
        default=True,
    )

    footer_title_1 = models.CharField(
        verbose_name='Título 1',
        max_length=100,
        blank=True,
        null=True,
    )

    footer_link_1 = models.CharField(
        verbose_name='Enlace interno 1',
        max_length=256,
        blank=True,
        null=True,
    )

    footer_image_1 = models.ImageField(
        verbose_name='Imagen 1',
        blank=True,
        null=True,
    )

    footer_title_2 = models.CharField(
        verbose_name='Título 2',
        max_length=100,
        blank=True,
        null=True,
    )

    footer_link_2 = models.CharField(
        verbose_name='Enlace interno 2',
        max_length=256,
        blank=True,
        null=True,
    )

    footer_image_2 = models.ImageField(
        verbose_name='Imagen 2',
        blank=True,
        null=True,
    )

    footer_title_3 = models.CharField(
        verbose_name='Título 3',
        max_length=100,
        blank=True,
        null=True,
    )

    footer_link_3 = models.CharField(
        verbose_name='Enlace interno 3',
        max_length=256,
        blank=True,
        null=True,
    )

    footer_image_3 = models.ImageField(
        verbose_name='Imagen 3',
        blank=True,
        null=True,
    )

    meta_title = models.CharField(
        max_length=55,
        help_text='Máximo 55 caracteres',
    )

    meta_description = models.CharField(
        max_length=115,
        help_text='Máximo 115 caracteres',
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    updated_at = models.DateTimeField(
        verbose_name='actualizado en',
        default=now,
    )

    is_active = models.BooleanField(
        verbose_name='¿está activa?',
        default=False,
    )

    video_url = models.URLField(
        blank=True,
        verbose_name='url de video de la página',
        help_text='Debe ser un video de youtube. Ej: https://www.youtube.com/'
        'watch?v=697EbMJei_Q',
    )

    @property
    def embed_video_url(self):
        from product.utils import embed_video
        return embed_video(self.video_url)

    def clean(self):
        depth = 0
        parent = self.parent
        while parent is not None:
            depth += 1
            parent = parent.parent
        if depth >= 4:
            raise ValidationError(
                'No se puede crear más de 4 niveles de páginas',
            )

        if self.show_children and strip_tags(self.content):
            raise ValidationError({
                'content': '''Si muestra los hijos no puede tener texto en el
                contenido'''
            })

    @property
    def get_parents(self):
        parents = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent
        parents.reverse()
        return parents

    @property
    def get_image(self):
        if self.image:
            return self.image
        parent = self.parent
        while parent.image or parent:
            if parent.image:
                return parent.image
            else:
                parent = parent.parent
        return self.parent.image

    def get_absolute_url(self):
        return reverse('cms:page_detail', args=(self.slug,))

    # Search Mixin
    @property
    def get_search_result_title(self):
        return self.title

    @property
    def get_search_result_description(self):
        return self.summary

    @property
    def get_search_result_image(self):
        return self.list_image or self.image

    @property
    def has_footer(self):
        return (
            self.footer_title_1 and self.footer_link_1 and
            self.footer_image_1 and self.footer_title_2 and
            self.footer_link_2 and self.footer_image_2 and
            self.footer_title_3 and self.footer_link_3 and self.footer_image_3
        )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'página'
        verbose_name_plural = 'páginas'
        unique_together = ('position', 'parent')
        ordering = ('-parent_id', 'position',)


class Gallery(models.Model):
    page = models.ForeignKey(
        'cms.Page',
        on_delete=models.CASCADE,
        related_name='gallery',
    )

    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    image = models.ImageField(
        max_length=256,
        upload_to='cms/gallery/',
        verbose_name='imagen',
    )

    position = models.PositiveIntegerField(
        verbose_name='posición',
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'galería de imágenes'
        verbose_name_plural = 'galerías de imágenes'
        ordering = ('position',)


class RelatedFile(models.Model):
    page = models.ForeignKey(
        'cms.Page',
        on_delete=models.CASCADE,
        related_name='related_files',
    )

    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    image = models.FileField(
        max_length=256,
        upload_to='cms/relatedfile/',
        verbose_name='archivo',
    )

    show_icon = models.BooleanField(
        verbose_name='mostrar ícono en lugar de enlace',
        default=False,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'archivo relacionado'
        verbose_name_plural = 'archivos relacionados'
        ordering = ('title',)


class RelatedLink(models.Model):
    page = models.ForeignKey(
        'cms.Page',
        on_delete=models.CASCADE,
        related_name='related_links',
    )

    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    url = models.URLField(
        verbose_name='enlace',
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'enlace relacionado'
        verbose_name_plural = 'enlaces relacionados'
        ordering = ('title',)


class CommunicationCategory(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    slug = AutoSlugField(
        populate_from='title',
        unique=True,
    )

    position = models.PositiveIntegerField(
        verbose_name='posición',
        unique=True,
    )

    has_comments = models.BooleanField(
        verbose_name='Comentarios habilitados',
        default=False,
    )

    has_share_buttons = models.BooleanField(
        verbose_name='Botones de compartir habilitados',
        default=False,
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de creación'
    )

    footer_title_1 = models.CharField(
        verbose_name='Título 1',
        max_length=100,
        blank=True,
        null=True,
    )

    footer_link_1 = models.CharField(
        verbose_name='Enlace interno 1',
        max_length=256,
        blank=True,
        null=True,
    )

    footer_image_1 = models.ImageField(
        verbose_name='Imagen 1',
        blank=True,
        null=True,
    )

    footer_title_2 = models.CharField(
        verbose_name='Título 2',
        max_length=100,
        blank=True,
        null=True,
    )

    footer_link_2 = models.CharField(
        verbose_name='Enlace interno 2',
        max_length=256,
        blank=True,
        null=True,
    )

    footer_image_2 = models.ImageField(
        verbose_name='Imagen 2',
        blank=True,
        null=True,
    )

    footer_title_3 = models.CharField(
        verbose_name='Título 3',
        max_length=100,
        blank=True,
        null=True,
    )

    footer_link_3 = models.CharField(
        verbose_name='Enlace interno 3',
        max_length=256,
        blank=True,
        null=True,
    )

    footer_image_3 = models.ImageField(
        verbose_name='Imagen 3',
        blank=True,
        null=True,
    )

    @property
    def has_footer(self):
        return (
            self.footer_title_1 and self.footer_link_1 and
            self.footer_image_1 and self.footer_title_2 and
            self.footer_link_2 and self.footer_image_2 and
            self.footer_title_3 and self.footer_link_3 and self.footer_image_3
        )

    def get_absolute_url(self):
        return reverse(
            'cms:communication_by_category_list',
            args=(self.slug,)
        )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'categoría de comunicación'
        verbose_name_plural = 'categorías de comunicación'
        ordering = ('position',)

    def clean(self):
        if self.title:
            unique_case_insensitive(self, 'title')


class Communication(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    category = models.ForeignKey(
        'cms.CommunicationCategory',
        on_delete=models.CASCADE,
        verbose_name='categoría',
    )

    image = models.ImageField(
        max_length=256,
        upload_to='cms/communication/',
        verbose_name='imagen del banner principal',
        help_text='La imagen debe tener el tamaño de 1920x469px',
    )

    list_image = models.ImageField(
        max_length=256,
        upload_to='cms/communication-list/',
        verbose_name='imagen para listados',
        help_text='El tamano de la imágen debe ser 520x680',
    )

    slug = AutoSlugField(
        populate_from='title',
        unique=True,
    )

    content = models.TextField(
        verbose_name='contenido de la página',
    )

    extended_content = models.TextField(
        verbose_name='contenido extendido de la página',
        blank=True,
    )

    event_date = models.DateField(
        verbose_name='fecha de inicio',
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        verbose_name='fecha de finalización',
        blank=True,
        null=True,
    )

    event_hour = models.CharField(
        max_length=15,
        verbose_name='hora del evento',
        blank=True,
        null=True,
    )

    event_city = models.CharField(
        max_length=100,
        verbose_name='sitio del evento',
        blank=True,
        null=True
    )

    event_place = models.CharField(
        max_length=100,
        verbose_name='lugar del evento',
        blank=True,
        null=True,
    )

    footer_title_1 = models.CharField(
        verbose_name='Título 1',
        max_length=100,
        blank=True,
        null=True,
    )

    footer_link_1 = models.CharField(
        verbose_name='Enlace interno 1',
        max_length=256,
        blank=True,
        null=True,
    )

    footer_image_1 = models.ImageField(
        verbose_name='Imagen 1',
        blank=True,
        null=True,
        help_text='El tamano de la imágen debe ser 991x122',
    )

    footer_title_2 = models.CharField(
        verbose_name='Título 2',
        max_length=100,
        blank=True,
        null=True,
    )

    footer_link_2 = models.CharField(
        verbose_name='Enlace interno 2',
        max_length=256,
        blank=True,
        null=True,
    )

    footer_image_2 = models.ImageField(
        verbose_name='Imagen 2',
        blank=True,
        null=True,
        help_text='El tamano de la imágen debe ser 991x122',
    )

    footer_title_3 = models.CharField(
        verbose_name='Título 3',
        max_length=100,
        blank=True,
        null=True,
    )

    footer_link_3 = models.CharField(
        verbose_name='Enlace interno 3',
        max_length=256,
        blank=True,
        null=True,
    )

    footer_image_3 = models.ImageField(
        verbose_name='Imagen 3',
        blank=True,
        null=True,
        help_text='El tamano de la imágen debe ser 991x122',
    )

    meta_title = models.CharField(
        max_length=55,
        help_text='Máximo 55 caracteres',
    )

    meta_description = models.CharField(
        max_length=115,
        help_text='Máximo 115 caracteres',
    )

    is_active = models.BooleanField(
        verbose_name='está activo',
        default=True,
    )

    has_contact = models.BooleanField(
        verbose_name='¿tiene contacto?',
        default=False,
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    updated_at = models.DateTimeField(
        verbose_name='actualizado en',
        default=now,
    )

    def get_absolute_url(self):
        return reverse(
            'cms:communication_detail',
            args=(self.slug,)
        )

    # Search Mixin
    @property
    def get_search_result_title(self):
        return self.title

    @property
    def get_search_result_description(self):
        return self.content

    @property
    def get_search_result_image(self):
        return self.list_image or self.image

    @property
    def has_footer(self):
        return (
            self.footer_title_1 and self.footer_link_1 and
            self.footer_image_1 and self.footer_title_2 and
            self.footer_link_2 and self.footer_image_2 and
            self.footer_title_3 and self.footer_link_3 and self.footer_image_3
        )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'comunicación'
        verbose_name_plural = 'comunicaciones'
        ordering = ('-created_at',)


class CommunicationGallery(models.Model):
    communication = models.ForeignKey(
        'cms.Communication',
        on_delete=models.CASCADE,
        related_name='gallery',
    )

    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    image = models.ImageField(
        max_length=256,
        upload_to='cms/communicationgallery/',
        verbose_name='imagen',
    )

    position = models.PositiveIntegerField(
        verbose_name='posición',
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'galería de imágenes'
        verbose_name_plural = 'galerías de imágenes'
        ordering = ('position',)


class CommunicationNewsManager(models.Manager):
    def get_queryset(self):
        return super(CommunicationNewsManager, self).get_queryset().exclude(
            category__slug='eventos',
        )


class CommunicationNews(Communication):
    objects = CommunicationNewsManager()

    class Meta:
        proxy = True
        ordering = ['-created_at']
        verbose_name_plural = 'comunicación'
        verbose_name = 'comunicaciones'


class CommunicationEventManager(models.Manager):
    def get_queryset(self):
        return super(CommunicationEventManager, self).get_queryset().filter(
            category__slug='eventos',
        )


class CommunicationEvent(Communication):
    objects = CommunicationEventManager()

    class Meta:
        proxy = True
        ordering = ['-created_at']
        verbose_name_plural = 'eventos'
        verbose_name = 'evento'


class CommunicationRelatedFile(models.Model):
    page = models.ForeignKey(
        'cms.Communication',
        on_delete=models.CASCADE,
        related_name='related_files',
    )

    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    image = models.FileField(
        max_length=256,
        upload_to='cms/communication-relatedfile/',
        verbose_name='archivo',
    )

    show_icon = models.BooleanField(
        verbose_name='mostrar ícono en lugar de enlace',
        default=False,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'archivo relacionado'
        verbose_name_plural = 'archivos relacionados'
        ordering = ('title',)


class SatelliteMonitoringContact(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name='nombre completo',
    )

    company = models.CharField(
        max_length=100,
        verbose_name='empresa',
    )

    email = models.EmailField(
        max_length=100,
        verbose_name='correo electrónico',
    )

    phone = models.CharField(
        max_length=100,
        verbose_name='teléfono',
    )

    address = models.CharField(
        max_length=100,
        verbose_name='dirección',
    )

    machine = models.CharField(
        max_length=100,
        verbose_name='tipo de máquina',
        help_text='Mencione al menos una serie de máquina que desea\
         monitorear'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        verbose_name = 'monitoreo satelital'
        verbose_name_plural = 'solicitudes de monitoreo'
        ordering = ('-created_at', 'name',)


class Block(models.Model):
    identifier = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Identificador',
    )

    content = models.TextField(
        verbose_name='Contenido',
    )

    image = models.ImageField(
        max_length=256,
        upload_to='cms/block/',
        verbose_name='Imagen del bloque.',
        help_text='El tamano de la imágen debe ser 500x400px',
        default='/',
    )

    url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Link del banner',
        help_text='E.G: http://youtube.com/',
    )

    is_active = models.BooleanField(
        verbose_name='¿está activo?',
        default=False,
    )

    def __str__(self):
        return '{0}'.format(self.identifier)

    class Meta:
        ordering = ['identifier']
        verbose_name = 'Bloque'
        verbose_name_plural = 'Bloques y Banners'


class FeaturedContent(models.Model):
    title = models.CharField(
        verbose_name='Título',
        max_length=64,
    )

    summary = models.TextField(
        verbose_name='Texto corto',
    )

    url = models.URLField(
        verbose_name='Enlace',
    )

    is_external = models.BooleanField(
        default=False,
        verbose_name='Es un enlace externo'
    )

    image = models.ImageField(
        max_length=256,
        upload_to='cms/featured-content/',
        verbose_name='Imagen del contenido destacado',
        help_text='El tamano de la imágen debe ser 1120x400px',
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = ['id']
        verbose_name = 'Contenido destacados del Home'
        verbose_name_plural = 'Contenidos destacados del Home'

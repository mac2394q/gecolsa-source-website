from django.db import models
from django.core.validators import RegexValidator


class SliderHome(models.Model):
    image_desktop = models.ImageField(
        max_length=256,
        upload_to='common/sliderhome/',
        verbose_name='imagen escritorio',
        help_text='2320x680 px PNG, JPG max 300 Kb',
    )

    image_mobile = models.ImageField(
        max_length=256,
        upload_to='common/sliderhome/',
        verbose_name='imagen mobile',
        help_text='1454x920 px PNG, JPG max 300 Kb',
    )

    image_tablet = models.ImageField(
        max_length=256,
        upload_to='common/sliderhome/',
        verbose_name='imagen tablet',
        help_text='1904x680 px PNG, JPG max 300 Kb',
    )

    url = models.CharField(
        max_length=256,
        verbose_name='enlace',
    )

    url_text = models.CharField(
        max_length=50,
        verbose_name='texto del enlace',
    )

    is_external = models.BooleanField(
        default=False,
        verbose_name='enlace externo',
    )

    position = models.PositiveIntegerField(
        verbose_name='posición',
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='está activo?',
    )

    class Meta:
        verbose_name = 'slider del home'
        verbose_name_plural = 'sliders del home'
        ordering = ('position',)


class Alliance(models.Model):
    """ Related allied that appear in home.
    """
    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    image = models.ImageField(
        max_length=256,
        upload_to='common/alliance/',
        verbose_name='imagen',
        help_text='La imagen debe tener el fondo blanco y 30 px de alto',
    )

    url = models.URLField(
        verbose_name='enlace',
    )

    position = models.PositiveIntegerField(
        verbose_name='posición',
        unique=True,
    )

    is_active = models.BooleanField(
        verbose_name='está activo',
        default=True,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'aliado'
        verbose_name_plural = 'aliados'
        ordering = ('position',)


class City(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'ciudad'
        verbose_name_plural = 'ciudades'
        ordering = ('title',)


class Office(models.Model):
    CATEGORY_RENT = 1
    CATEGORY_FINANCE = 2
    CATEGORY_GECOLSA = 3
    CATEGORY_RELIANZ = 4
    CATEGORY_CHOICES = (
        (CATEGORY_RENT, 'Renta'),
        (CATEGORY_FINANCE, 'Financiación'),
        (CATEGORY_GECOLSA, 'Gecolsa'),
        (CATEGORY_RELIANZ, 'Relianz'),
    )

    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    category = models.PositiveSmallIntegerField(
        verbose_name='categoría',
        choices=CATEGORY_CHOICES,
    )

    city = models.ForeignKey(
        'common.City',
        on_delete=models.CASCADE,
        verbose_name='ciudad',
        related_name='offices'
    )

    latlon = models.CharField(
        max_length=100,
        verbose_name='posición',
        validators=[RegexValidator(
            regex=r'^[-+]?[0-9]*\.?[0-9]+, [-+]?[0-9]*\.?[0-9]+$'
        )],
        help_text='Bogotá es: -74.18132, 4.31454'
    )

    phone = models.CharField(
        max_length=100,
        verbose_name='teléfono',
    )

    address = models.CharField(
        max_length=100,
        verbose_name='dirección',
    )

    schedule = models.TextField(
        verbose_name='horario',
    )

    is_active = models.BooleanField(
        verbose_name='está activo',
        default=True,
    )

    def get_lat(self):
        return self.latlon.split(',')[-1]

    def get_lon(self):
        return self.latlon.split(',')[0]

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'oficina'
        verbose_name_plural = 'oficinas'
        ordering = ('title',)


class FixedBlock(models.Model):
    """ Blocks used to show content on templates.
    """
    image = models.ImageField(
        max_length=256,
        upload_to='common/fixedblock/',
        verbose_name='imagen',
        help_text='El tamaño de la imagen debe ser de 1400 x 600 pixeles',
    )

    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    slug = models.SlugField(
        unique=True,
    )

    summary = models.TextField(
        verbose_name='resumen',
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'bloque fijo'
        verbose_name_plural = 'bloques fijos'
        ordering = ('title',)


class ImageLink(models.Model):
    """ Images with a related link used in categories.
    """
    SECTION_CHOICES = (
        ('communication', 'Comunicación'),
        ('contact', 'Contacto'),
        ('home', 'Home'),
        ('merchandise', 'Merchandise'),
        ('new-equipment', 'Nuevos'),
        ('office-list', 'Sedes'),
        ('subscribe', 'Suscripción'),
        ('used-equipment', 'Usados'),
    )

    image = models.ImageField(
        max_length=256,
        upload_to='common/imagelink/',
        verbose_name='imagen',
    )

    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    section = models.CharField(
        max_length=100,
        choices=SECTION_CHOICES,
        verbose_name='section',
    )

    url = models.CharField(
        max_length=256,
        verbose_name='enlace',
    )

    is_external = models.BooleanField(
        default=False,
        verbose_name='enlace externo',
    )

    position = models.PositiveIntegerField(
        verbose_name='posición',
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'imagen de enlace'
        verbose_name_plural = 'imágenes de enlace'
        ordering = ('position',)


class CompanyType(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='título',
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'tipo de industria'
        verbose_name_plural = 'tipos de industria'
        ordering = ('title',)


class Contact(models.Model):
    """ Stores contact form info.
    """
    CATEGORY_CONTACT_MAIN = 1
    CATEGORY_CONTACT_CLAIMS = 2
    CATEGORY_CONTACT_SALES = 3
    CATEGORY_CONTACT_OTHERS = 4
    CATEGORY_CONTACT_CHOICES = (
        (CATEGORY_CONTACT_MAIN, 'Contacto'),
        (CATEGORY_CONTACT_CLAIMS, 'Quejas y reclamos'),
        (CATEGORY_CONTACT_SALES, 'Asesoría comercial'),
        (CATEGORY_CONTACT_OTHERS, 'Otros asuntos'),
    )

    CATEGORY_BY_EMAIL = 10
    CATEGORY_BY_PHONE = 20
    CONTACT_BY_CHOICES = (
        (CATEGORY_BY_EMAIL, 'Email'),
        (CATEGORY_BY_PHONE, 'Teléfono'),
    )

    name = models.CharField(
        max_length=255,
        verbose_name='nombre',
    )

    mobile_number = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='celular',
    )

    email = models.EmailField(
        max_length=255,
        verbose_name='e-mail',
    )

    recipients = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='categorias y correos',
    )

    comment = models.TextField(
        verbose_name='comentario',
    )

    contact_by = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='tipo de contacto',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='creado en',
    )

    full_path = models.CharField(
        max_length=255,
        verbose_name='URL de origen',
        blank=True,
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'mensaje de contacto'
        verbose_name_plural = 'mensajes de contacto'
        ordering = ('-id',)


class WsLog(models.Model):
    """ Logging of webservices and results
    """

    endpoint = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='url',
    )

    status_code = models.PositiveSmallIntegerField(
        verbose_name='código resultado'
    )

    request_data = models.TextField(
        verbose_name='envío',
        blank=True,
    )

    answer_data = models.TextField(
        verbose_name='respuesta',
        blank=True,
    )

    ellapsed_time = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='tiempo de consulta'
    )

    category = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='categoría',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='creado en',
    )

    def __str__(self):
        return '{0}'.format(self.category)

    class Meta:
        verbose_name = 'log de webservice'
        verbose_name_plural = 'logs de webservices'
        ordering = ('-created_at',)

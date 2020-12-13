from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models

from app.storages import get_upload_path
from app.validators import FileSizeValidator

from . import data


class RequestComplaint(models.Model):
    type_complaint = models.PositiveSmallIntegerField(
        choices=data.TYPE_COMPLAINT_CHOICES,
        verbose_name='¿la denuncia se realizará de manera anónima?',
        default=data.ANONYMOUS_CHOICE,
    )

    full_name = models.CharField(
        max_length=80,
        verbose_name='nombres y apellidos',
        blank=True
    )

    email = models.EmailField(
        verbose_name='correo electrónico',
        help_text='Máximo 100 caracteres',
        max_length=60,
        blank=True
    )

    phone_number = models.CharField(
        max_length=10,
        verbose_name='Número de contacto',
        blank=True,
        validators=[
            RegexValidator(r'^[0-9]*$', message='Ingresa solo números'),
            MinLengthValidator(
                settings.PHONE_NUMBER_LENGTH,
                message='Asegurate que tenga al menos {} caracteres'.format(
                    settings.PHONE_NUMBER_LENGTH
                )
            ),
        ],
    )

    company_relation = models.CharField(
        max_length=100,
        verbose_name='vínculo con la compañía'
    )

    purpose = models.CharField(
        max_length=100,
        verbose_name='objeto de la denuncia'
    )

    date = models.DateField(
        verbose_name='fecha de los hechos'
    )

    place = models.CharField(
        max_length=100,
        verbose_name='lugar de los hechos'
    )

    acts = models.TextField(
        verbose_name='hechos de la denuncia',
        help_text='Identificar si los hechos están por suceder'
    )

    people_complaint = ArrayField(
        models.CharField(max_length=80),
        verbose_name='persona(s) denunciada(s)'
    )

    document = models.FileField(
        upload_to=get_upload_path,
        verbose_name='documento adjunto',
        validators=[FileSizeValidator(2000)],
        help_text='máximo 2MB',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha de creación',
    )

    def is_anonymous(self):
        return self.type_complaint == data.ANONYMOUS_CHOICE

    def get_people_complaint(self):
        return ', '.join(self.people_complaint)

    def __str__(self):
        return self.purpose

    class Meta:
        ordering = ['-id']
        verbose_name = 'queja'
        verbose_name_plural = 'quejas y reclamos'

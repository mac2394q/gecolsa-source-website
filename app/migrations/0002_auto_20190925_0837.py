# Generated by Django 2.0.7 on 2019-09-25 13:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestcomplaint',
            name='other_relation',
        ),
        migrations.AlterField(
            model_name='requestcomplaint',
            name='company_relation',
            field=models.CharField(max_length=100, verbose_name='vínculo con la compañía'),
        ),
        migrations.AlterField(
            model_name='requestcomplaint',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Ingresa solo números'), django.core.validators.MinLengthValidator(7, message='Asegurate que tenga al menos 7 caracteres')], verbose_name='Número de contacto'),
        ),
        migrations.AlterField(
            model_name='requestcomplaint',
            name='type_complaint',
            field=models.PositiveSmallIntegerField(choices=[(10, 'Sí'), (20, 'No')], default=10, verbose_name='¿la denuncia se realizará de manera anónima?'),
        ),
    ]

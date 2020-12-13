# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-16 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_contactcategory_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='contact_by',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(10, 'Email'), (20, 'Teléfono')], default=10, verbose_name='tipo de contacto'),
        ),
    ]

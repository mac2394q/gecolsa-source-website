# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_contact_full_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contact_by',
            field=models.CharField(blank=True, max_length=300, verbose_name='categorias y correos'),
        ),
    ]

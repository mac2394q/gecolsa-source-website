# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-20 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactcategory',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='está activo'),
        ),
    ]

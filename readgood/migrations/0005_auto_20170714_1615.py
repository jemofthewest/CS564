# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('readgood', '0004_auto_20170713_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveSmallIntegerField(),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outlets', '0005_outlet_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outlet',
            name='last_update',
        ),
        migrations.RemoveField(
            model_name='outlet',
            name='toy_types',
        ),
        migrations.AddField(
            model_name='outlet',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]

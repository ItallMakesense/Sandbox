# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 16:23
from __future__ import unicode_literals

from django.db import migrations, models
import outlets.validators


class Migration(migrations.Migration):

    dependencies = [
        ('outlets', '0006_auto_20171003_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='category',
            field=models.CharField(blank=True, max_length=120, null=True, validators=[outlets.validators.validate_category]),
        ),
    ]

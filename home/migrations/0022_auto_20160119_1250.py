# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 12:50
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20160119_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logomaker',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='logo', to='home.EventsPage'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-18 13:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20160118_1012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventspage',
            old_name='topicTag',
            new_name='tag',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-18 10:12
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20160117_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='credit',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
    ]

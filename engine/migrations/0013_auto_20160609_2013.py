# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0012_auto_20160609_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='url',
            field=models.URLField(blank=True, default=''),
        ),
    ]
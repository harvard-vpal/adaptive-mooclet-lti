# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 20:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0002_auto_20160825_1628'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mooclettype',
            old_name='content_type',
            new_name='parent_content_type',
        ),
    ]
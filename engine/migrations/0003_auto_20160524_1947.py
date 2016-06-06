# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 19:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('engine', '0002_auto_20160521_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.CharField(default='', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseUserState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.CourseUser')),
            ],
        ),
        migrations.CreateModel(
            name='CourseUserVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='order',
        ),
        migrations.AlterField(
            model_name='quiz',
            name='url',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='courseuserstate',
            name='variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.CourseUserVariable'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 09:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('url', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_created', to=settings.AUTH_USER_MODEL)),
                ('user_like', models.ManyToManyField(blank=True, related_name='images_liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

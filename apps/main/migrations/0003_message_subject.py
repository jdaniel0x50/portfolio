# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-19 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.CharField(default='Portfolio FollowUp', max_length=100),
        ),
    ]

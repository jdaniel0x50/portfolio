# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-20 22:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180120_1545'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectImages',
            new_name='ProjectImage',
        ),
    ]

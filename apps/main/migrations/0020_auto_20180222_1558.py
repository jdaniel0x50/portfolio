# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-22 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20180220_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillimage',
            name='skill',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Skill'),
        ),
    ]
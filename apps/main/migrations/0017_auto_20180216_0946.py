# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-16 09:46
from __future__ import unicode_literals

import apps.main.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_skill_logo_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=apps.main.models.skill_logo_directory_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='skill',
            name='logo_img',
        ),
        migrations.AddField(
            model_name='skillimage',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Skill'),
        ),
    ]
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Skill, Project, ProjectImage, Message

# Register your models here
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(Message)

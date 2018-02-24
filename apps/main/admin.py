# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Skill, Project, ProjectImage, Message
from ..db_admin._resume.models import Resume
from ..db_admin._traffic.models import Traffic

# Register your models here
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(Message)
admin.site.register(Resume)
admin.site.register(Traffic)

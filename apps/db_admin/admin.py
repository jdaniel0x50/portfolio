# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ._resume.models import Resume
from ._traffic.models import Traffic

admin.site.register(Resume)
admin.site.register(Traffic)

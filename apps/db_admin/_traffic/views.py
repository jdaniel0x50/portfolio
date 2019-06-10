# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

import portfolio.settings_environ as settings_environ
if settings_environ.PERMISSION_REQUIRED != None:
    from portfolio.settings_environ import PERMISSION_REQUIRED
else:
    from portfolio.settings_sensitive import PERMISSION_REQUIRED

from datetime import datetime
from .models import Traffic



@login_required
@permission_required(PERMISSION_REQUIRED, raise_exception=True)
def traffic_index(request, sort_f="none"):
    Traffic.objects.filter(date_visited__lt=datetime(2018,2,24)).delete()
    traffic = Traffic.objects.get_all(sort_f)
    totals = Traffic.objects.get_total()
    
    context = {
        'traffic': traffic,
        'totals': totals,
    }
    return render(request, "db_traffic/index.html", context)

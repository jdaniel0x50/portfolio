# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required, permission_required

from datetime import datetime
from .models import Traffic



@login_required
@permission_required('auth.user.can_add_user', raise_exception=True)
def traffic_index(request, sort_f="none"):
    Traffic.objects.filter(date_visited__lt=datetime(2018,2,24)).delete()
    traffic = Traffic.objects.get_all(sort_f)
    totals = Traffic.objects.get_total()
    
    context = {
        'traffic': traffic,
        'totals': totals,
    }
    return render(request, "db_traffic/index.html", context)


@login_required
@permission_required('auth.user.can_add_user', raise_exception=True)
def test_perm(request):
    return render(request, 'db_traffic/test.html')
    
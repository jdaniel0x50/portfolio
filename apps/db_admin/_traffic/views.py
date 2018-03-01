# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_list_or_404
from ...main.exceptions import const, method_not_allowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from datetime import datetime

from .models import Traffic

def traffic_index(request, sort_f="none"):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)

    Traffic.objects.filter(date_visited__lt=datetime(2018,2,24)).delete()
    traffic = Traffic.objects.get_all(sort_f)
    totals = Traffic.objects.get_total()
    
    context = {
        'traffic': traffic,
        'totals': totals,
    }
    return render(request, "db_traffic/index.html", context)

@login_required
@permission_required('db_admin.traffic.can_add_traffic')
def test_perm(request):
    return render(request, 'db_traffic/test.html')
    
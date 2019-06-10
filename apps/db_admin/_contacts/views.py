# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

import portfolio.settings_environ as settings_environ
if settings_environ.PERMISSION_REQUIRED != None:
    from portfolio.settings_environ import PERMISSION_REQUIRED
else:
    from portfolio.settings_sensitive import PERMISSION_REQUIRED

from .models import Contact


@login_required
@permission_required(PERMISSION_REQUIRED, raise_exception=True)
def contact_index(request, sort_f="none"):
    # get all contacts currently in the database
    contacts = Contact.objects.get_all(sort_f)
    contact_totals = Contact.objects.get_total()

    # logged in user
    context = {
        'contacts': contacts,
        'contact_totals': contact_totals,
    }
    return render(request, 'db_contacts/index.html', context)


@login_required
@permission_required(PERMISSION_REQUIRED, raise_exception=True)
def destroy_contact(request, id):
    Contact.objects.get(id=id).delete()
    return redirect(reverse('db_admin:contacts'))

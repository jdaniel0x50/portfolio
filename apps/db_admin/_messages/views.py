# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from ...main.exceptions import const

from ...main.models import Message


def message_index(request, sort_f="none"):
    if not request.user.is_authenticated():
        # if not admin_user_confirm(request):
        return redirect(const.redirect_403)

    # get all messages currently in the database
    # translate the sort field to a model field
    translator = {
        "none": "none",
        "sender": "sender_name",
        "-sender": "-sender_name",
        "from_email": "sender_email",
        "-from_email": "-sender_email",
        "subject": "subject",
        "-subject": "-subject",
        "date": "message_sent",
        "-date": "-message_sent"
    }
    sort_model = translator[sort_f]
    emails = Message.objects.get_all(sort_model)
    email_totals = Message.objects.get_total()

    # logged in user
    context = {
        'emails': emails,
        'email_totals': email_totals,
    }
    return render(request, 'db_messages/index.html', context)


def destroy_message(request, id):
    if not request.user.is_authenticated():
        # if not admin_user_confirm(request):
        return redirect(const.redirect_403)

    Message.objects.get(id=id).delete()
    return redirect(reverse('db_admin:messages'))

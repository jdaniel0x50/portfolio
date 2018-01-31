# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# local app-specific imports
from django.shortcuts import render, redirect

# import forms and related modules
from django import forms
from django.forms.utils import ErrorList
from django.contrib import messages
from .forms import NewAdminForm, NewSkillForm
from ..main.exceptions import admin_user_confirm, const
from django.shortcuts import get_object_or_404

# import related models
from .models import User
from ..main.models import Skill, Message


def construct_session_context(request):
    # use this function to construct the logged in user context
    context = {}
    if 'user_id' in request.session:
        context = {
            "username": request.session['username'],
            "user_first": request.session['user_first']
        }
    return context


def admin_access_denied(request):
    return redirect('/')


def admin_index(request):
    # check if the user previously submitted a form with errors
    if 'form_values' in request.session:
        # create a new form instance with the values stored in session
        # for key in request.session['form_values']:
        #     form[key].value = request.session['form_values'][key]
        form = NewAdminForm(request.session['form_values'])

        # create errors to view on the template
        form.is_valid()
        del request.session['form_values']
    else:
        form = NewAdminForm()
    user = construct_session_context(request)
    return render(request, 'db_admin/index.html', {'form': form, 'user': user})


def admin_login(request):
    result = User.objects.login_validator(request, request.POST)
    # result is a dictionary object with errors and user, if successful
    errors = result['errors']
    if len(errors):
        # the validator returned errors
        for err in errors:
            extra_tags = err['tag']
            messages.error(request, err['message'], extra_tags=extra_tags)
        return redirect('/admin')
    else:
        # no errors, login and proceed to first page
        user = result['user']
        request.session['user_id'] = user['id']
        request.session['username'] = user['username']
        request.session['user_first'] = user['first_name']
        first_page = '/admin/skill/index'
        return redirect(first_page)


def admin_logout(request):
    if not admin_user_confirm(request):
        return redirect(const.redirect_403)
    try:
        del request.session['user_id']
        del request.session['username']
        del request.session['user_first']
    except KeyError:
        pass
    return redirect('/')


# def create_admin(request):
#     # setup return and redirect routes
#     redirect_error_route = "/admin/"
#     redirect_success_route = "/"

#     # use forms.py to validate form data
#     form = NewAdminForm(request.POST)
#     if form.is_valid():
#         # form data is valid
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         password = User.objects.hash_password(request.POST['password'])
#         user = User.objects.create(
#             username=username, 
#             first_name=first_name, 
#             last_name=last_name, 
#             password=password
#         )
#         request.session['user_id'] = user.id
#         request.session['username'] = user.username
#         request.session['user_first'] = user.first_name
#         return redirect(redirect_success_route)
#     else:
#         # form data has validation errors
#         form_values = form.cleaned_data
#         request.session['form_values'] = form_values
#         return redirect(redirect_error_route)
        


def skills_index(request, sort_f="none"):
    if not admin_user_confirm(request):
        return redirect(const.redirect_403)

    # check if the user previously submitted a form with errors
    if 'form_values' in request.session:
        # create a new form instance with the values stored in session
        form = NewSkillForm(request.session['form_values'])

        # create errors to view on the template
        form.is_valid()
        del request.session['form_values']
    else:
        # generate new skill form template
        form = NewSkillForm()

    # translate the sort field to a model field
    translator = {
        "none": "none",
        "skill": "skill_name",
        "-skill": "-skill_name",
        "category": "skill_type",
        "-category": "-skill_type",
        "level": "skill_level",
        "-level": "-skill_level",
        "date": "created_at",
        "-date": "-created_at"
    }
    sort_model = translator[sort_f]
    # get all skills currently in the database
    skills = Skill.objects.get_all(sort_model)
    skills_totals = Skill.objects.get_total()

    # logged in user
    user = construct_session_context(request)

    context = {
        'form': form,
        'skills': skills,
        'skills_totals': skills_totals,
        'user': user
    }
    return render(request, 'db_admin/skills_index.html', context)


def skills_create(request):
    if not admin_user_confirm(request):
        return redirect(const.redirect_403)

    # setup return and redirect routes
    redirect_error_route = "/admin/skill/index"
    redirect_success_route = "/admin/skill/index"

    # use forms.py to validate form data
    form = NewSkillForm(request.POST)
    if form.is_valid():
        # form data is valid
        skill_name = request.POST['skill_name']
        skill_type = request.POST['skill_type']
        logo_url = request.POST['logo_url']
        skill_level = request.POST['skill_level']

        skill = Skill.objects.create(
            skill_name=skill_name,
            skill_type=skill_type,
            logo_url=logo_url,
            skill_level=skill_level
        )
        return redirect(redirect_success_route)
    else:
        # form data has validation errors
        form_values = form.cleaned_data
        request.session['form_values'] = form_values
        return redirect(redirect_error_route)


def message_index(request, sort_f="none"):
    if not admin_user_confirm(request):
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
    user = construct_session_context(request)
    context = {
        'emails': emails,
        'email_totals': email_totals,
        'user': user
    }
    return render(request, 'db_admin/messages_index.html', context)


def destroy_message(request, id):
    if not admin_user_confirm(request):
        return redirect(const.redirect_403)

    Message.objects.get(id=id).delete()
    return redirect('/admin/message/index')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from ...main.exceptions import const, method_not_allowed

from ...main.models import Skill, SkillImage
from .forms import NewSkillForm, NewSkillImageForm


def skills_index(request, sort_f="none"):
    if not request.user.is_authenticated():
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

    # # logged in user
    # user = construct_session_context(request)

    context = {
        'form': form,
        'skills': skills,
        'skills_totals': skills_totals,
        # 'user': user
    }
    return render(request, 'db_skills/index.html', context)


def skills_create(request):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)

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
    else:
        # form data has validation errors
        form_values = form.cleaned_data
        request.session['form_values'] = form_values
    return redirect(reverse('db_admin:skills'))


def skill_destroy(request, id):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)
    print "INSIDE SKILL DESTROY ACTION"
    images = SkillImage.objects.filter(skill=id)
    for image in images:
        image.delete()      # remove project images
    Skill.objects.get(id=id).delete()
    return redirect(reverse('db_admin:skills'))


def skill_logo(request, id):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)

    if request.method == 'POST':
        _xHeader = {
            'value': 'False',
            'label': 'X-Form-Errors',   # documents whether form has errors
        }
        result = {
            'title': "",
            'message': ""
        }

        form = NewSkillImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            result['title'] = "Upload Saved"
            result['message'] = "The image was successfully uploaded."
            html = render_to_string('db_projects/edit_response.html', result)
        else:
            # errors in the form submission
            _xHeader['value'] = 'True'
            images = SkillImage.objects.get_by_skill(id)
            context = {
                'form': form,
                'skill_id': id,
                'images': images,
                'form_errors': True
            }
            html = render_to_string('db_skills/add_logo.html', context, request)

        _http_response = HttpResponse(html)
        _http_response.__setitem__(_xHeader['label'], _xHeader['value'])
        return _http_response
    
    elif request.method == 'GET':
        # get logo image and render form
        images = SkillImage.objects.get_by_skill(id)
        context = {
            'skill_id': id,
            'images': images,
        }
        html = render_to_string('db_skills/add_logo.html', context, request)
        return HttpResponse(html)
    else:
        response = method_not_allowed(request)
        return response


def skill_logo_destroy(request, id, logo_id):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)
    print "INSIDE LOGO DESTROY ACTION"
    img = get_object_or_404(SkillImage, id=logo_id)
    img.delete()

    images = SkillImage.objects.get_by_skill(id)
    context = {
        'skill_id': id,
        'images': images,
    }
    html = render_to_string('db_skills/add_logo.html', context, request)
    return HttpResponse(html)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# local app-specific imports
import json
from datetime import date, datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from ...main.exceptions import method_not_allowed, const

# import forms and related modules
from django import forms
from django.forms.utils import ErrorList
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import NewProjectForm, NewImageForm, EditImageForm

# import related models
from django.shortcuts import get_object_or_404
from ...main.models import Skill, Project, ProjectImage


def projects_index(request, sort_f="none"):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)

    # check if the user previously submitted a form with errors
    errors = False
    if 'form_values' in request.session:
        # create a new form instance with the values stored in session
        form = NewProjectForm(request.session['form_values'])

        # create errors to view on the template
        form.is_valid()
        errors = True
        del request.session['form_values']
    else:
        # generate new form template
        form = NewProjectForm()

    # translate the sort field to a model field
    translator = {
        "none": "none",
        "project": "project_name",
        "-project": "-project_name",
        "order": "feat_order",
        "-order": "-feat_order",
        "level": "skill_level",
        "-level": "-skill_level",
        "date": "project_timeline",
        "-date": "-project_timeline"
    }
    sort_model = translator[sort_f]
    # get all projects currently in the database
    projects = Project.objects.get_all(sort_model)

    context = {
        'form': form,
        'errors': errors,
        'projects': projects,
    }
    return render(request, 'db_projects/index.html', context)


def projects_create(request):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)

    # use forms.py to validate form data
    form_context = {
        'project_name': request.POST['project_name'],
        'subtitle': request.POST['subtitle'],
        'description': request.POST['description'],
        'impact': request.POST['impact'],
        'project_timeline': request.POST['project_timeline'],
        'feat_order': request.POST['feat_order'],
        'deploy_url': request.POST['deploy_url'],
        'code_url': request.POST['code_url'],
        'skills': request.POST.getlist('skills')
    }
    form = NewProjectForm(form_context)
    if form.is_valid():
        # form data is valid
        project = Project.objects.create(
            project_name=form_context['project_name'],
            description=form_context['description'],
            project_timeline=form_context['project_timeline'],
            feat_order=form_context['feat_order'],
            impact=form_context['impact'],
            deploy_url=form_context['deploy_url'],
            code_url=form_context['code_url'],
        )

        # create array of skill objects and many-to-many relationship
        for skill in form_context['skills']:
            skill_obj = Skill.objects.get(id=skill)
            project.skills.add(skill_obj)
        project.save()
    else:
        # form data has validation errors
        request.session['form_values'] = form_context
    return redirect(reverse('db_admin', 'projects'))


def project_edit(request, id):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)

    if request.method == "GET":
        # GET project for edit form; returns a partial view
        project = Project.objects.get(id=id)
        form_context = {
            'project_name': project.project_name,
            'subtitle': project.subtitle,
            'description': project.description,
            'impact': project.impact,
            'feat_order': project.feat_order,
            'deploy_url': project.deploy_url,
            'code_url': project.code_url,
        }
        form_context['project_timeline'] = project.project_timeline.isoformat()
        skills = []
        for skill in project.skills.all():
            skills.append(skill.id)
        form_context['skills'] = skills
        edit_form = NewProjectForm(form_context)
        request.session['form_data'] = edit_form.data

        context = {
            'project': project,
            'edit_form': edit_form,
        }
        html = render_to_string("db_projects/edit_form.html", context, request)
        return HttpResponse(html)
    
    if request.method == "POST":
        # POST updated project from edit form
        # use forms.py to validate form data
        initial_data = request.session['form_data']
        del request.session['form_data']
        form_data = {}
        skills = request.POST.getlist('skills')
        form_data['skills'] = skills

        for key in request.POST:
            if key == 'skills': continue
            if request.POST[key] == "on": continue
            form_data[key] = request.POST[key]

        # set html and header variables
        html = ""
        _xHeader = {
            'value': 'False',
            'label': 'X-Form-Errors',   # documents whether form has errors
        }
        result = {
            'title': "",
            'message': ""
        }

        project = get_object_or_404(Project, id=id)
        form = NewProjectForm(form_data, initial=initial_data)
        if form.has_changed():
            # there were changes in the form submission
            if form.is_valid():
                result['title'] = "Changes Saved"
                for field in form.changed_data:
                    setattr(project, field, form_data[field])
                    result['message'] += "<div class='row col-sm-12'>" \
                                        + "<p class='text-dark'><strong>" \
                                        + form[field].label \
                                        + "</strong> changed"
                    if field != 'skills':
                        result['message'] += " to <span class='text-danger'>" \
                                            + "<strong><em>" \
                                            + form_data[field] \
                                            + "</em></strong></span>"
                    result['message'] += "</p></div>"
                
                if 'skills' in form.changed_data:
                    form.changed_data.remove('skills')
                project.save(update_fields=form.changed_data)

                # generate html partial from result
                html = render_to_string('db_projects/edit_response.html', result)
            else:
                # form data has validation errors
                request.session['form_data'] = form.data
                context = {
                    'project': project,
                    'edit_form': form,
                    'edit_errors': True
                }
                html = render_to_string("db_projects/edit_form.html", context, request)
                _xHeader['value'] = 'True'
        else:
            # no changes in form submission
            result['title'] = "No Changes"
            result['message'] = "No changes submitted"
            html = render_to_string('db_projects/edit_response.html', result)

    # return success or error html partial with custom header
    _http_response = HttpResponse(html)
    for header in _xHeader:
        _http_response.__setitem__(_xHeader['label'], _xHeader['value'])
    return _http_response


def img_upload(request, id):
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

        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            result['title'] = "Upload Saved"
            result['message'] = "The image was successfully uploaded."
            html = render_to_string('db_projects/edit_response.html', result)
        else:
            # errors in the form submission
            _xHeader['value'] = 'True'
            project = Project.objects.get(id=id)
            context = {
                'form': form,
                'project': project,
                'form_errors': True
            }
            html = render_to_string(
                'db_projects/edit_img_add.html', context, request)

        _http_response = HttpResponse(html)
        _http_response.__setitem__(_xHeader['label'], _xHeader['value'])
        return _http_response
    else:
        form = NewImageForm()
        project = Project.objects.get(id=id)
        context = {
            'form': form,
            'project': project,
        }
        html = render_to_string('db_projects/edit_img_add.html', context, request)
        return HttpResponse(html)


def img_getall(request, id):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)

    project = Project.objects.get(id=id)
    images = ProjectImage.objects.get_all_project(id)
    context = {
        'project': project,
        'images': images
    }
    html = render_to_string('db_projects/edit_img_list.html', context, request)
    return HttpResponse(html)


def img_edit(request, id, image_id):
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

        instance = get_object_or_404(ProjectImage, id=image_id)
        form = EditImageForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            result['title'] = "Updates Saved"
            result['message'] = "The image was successfully updated."
            html = render_to_string('db_projects/edit_response.html', result)
        else:
            # errors in the form submission
            _xHeader['value'] = 'True'
            project = get_object_or_404(Project, id=id)
            title = ("Editing Image "
                    + "<small><u>"
                    + instance.filename()
                    + "</u> for <strong>"
                    + project.project_name
                    + "</small></strong>")
            context = {
                'title': title,
                'form': form,
                'image': instance,
                'project': project,
                'form_errors': True
            }
            html = render_to_string(
                'db_projects/edit_img_add.html', context, request)

        _http_response = HttpResponse(html)
        _http_response.__setitem__(_xHeader['label'], _xHeader['value'])
        return _http_response
    elif request.method == 'GET':
        image = get_object_or_404(ProjectImage, id=image_id)
        project = get_object_or_404(Project, id=id)
        form = EditImageForm(image)
        title = ("Editing Image " 
                + "<small><u>"
                + image.filename() 
                + "</u> for <strong>"
                + project.project_name
                + "</small></strong>")
        context = {
            'title': title,
            'form': form,
            'image': image,
            'project': project,
        }
        html = render_to_string(
            'db_projects/edit_img_edit.html', context, request)
        return HttpResponse(html)
    else:
        response = method_not_allowed(request)
        return response


def img_mark_feature(request, id, image_id):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)

    if request.method == "POST":
        project = get_object_or_404(Project, id=id)
        image = get_object_or_404(ProjectImage, id=image_id)
        project.featimage_url = image.img_url
        project.save()
        return HttpResponse("success")
    else:
        response = method_not_allowed(request)
        return response

def destroy_project(request, id):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)

    images = ProjectImage.objects.filter(project=id)
    for image in images:
        image.delete()      # remove project images
    Project.objects.get(id=id).delete()
    return redirect(reverse('projects'))


def destroy_image(request, id, image_id):
    if not request.user.is_authenticated():
        return redirect(const.redirect_403)
    
    ProjectImage.objects.remove(image_id)
    # ProjectImage.objects.get(id=image_id).delete()
    return HttpResponse("success")

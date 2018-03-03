# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

import portfolio.settings_environ as settings_environ
if settings_environ.PERMISSION_REQUIRED != None:
    from portfolio.settings_environ import PERMISSION_REQUIRED
else:
    from portfolio.settings_sensitive import PERMISSION_REQUIRED

from .models import Resume
from .forms import UploadResumeForm



@login_required
def index(request):
    resumes = Resume.objects.get_all()
    context = {
        "resumes": resumes
    }
    return render(request, 'db_resume/index.html', context)


@login_required
@permission_required(PERMISSION_REQUIRED, raise_exception=True)
def upload(request):
    if request.method == 'POST':
        _xHeader = {
            'value': 'False',
            'label': 'X-Form-Errors',   # documents whether form has errors
        }
        result = {
            'title': "",
            'message': ""
        }

        form = UploadResumeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            result['title'] = "Upload Saved"
            result['message'] = "The file was successfully uploaded."
            html = render_to_string('db_projects/edit_response.html', result)
        else:
            # errors in the form submission
            _xHeader['value'] = 'True'
            context = {
                'form': form,
                'form_errors': True
            }
            html = render_to_string('db_resume/create.html', context, request)

        _http_response = HttpResponse(html)
        _http_response.__setitem__(_xHeader['label'], _xHeader['value'])
        return _http_response
    return redirect(reverse('db_admin:resume'))


@login_required
def list(request):
    resumes = Resume.objects.get_all()
    context = {
        "resumes": resumes
    }
    http = render_to_string('db_resume/list.html', context, request)
    return HttpResponse(http)


@login_required
@permission_required(PERMISSION_REQUIRED, raise_exception=True)
def destroy(request, id):
    res = get_object_or_404(Resume, id=id)
    res.delete()
    return redirect(reverse('db_admin:resume'))
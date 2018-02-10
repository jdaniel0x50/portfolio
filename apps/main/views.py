# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from portfolio.settings_environ import DEFAULT_FROM_EMAIL

from django.shortcuts import get_object_or_404
from .models import Skill, Project, ProjectImage, Message

# import path to get content from text files to import to templates
import os
from portfolio.settings import BASE_DIR
_file_path = os.path.join(BASE_DIR, 'content_files')

# import settings to handle static files in development (no cache)
from django.views.static import serve as staticserve
import portfolio.settings as settings

# import requests module for api call
import requests

# import forms for email message form
from django import forms
from django.forms.utils import ErrorList
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from .forms import NewMessageForm


def main_page(request):
    # on load, clear recaptcha if currently in session
    if 'recaptcha' in request.session:
        del request.session['recaptcha']

    print "*** STARTING PAGE LOAD ***"
    print "Base Directory: " + BASE_DIR
    print "Project Root: " + settings.PROJECT_ROOT
    print "Static Root: " + settings.STATIC_ROOT
    try:
        import settings_deploy as deployed
        print deployed.DEBUG
        print deployed.MEDIA_ROOT
        print deployed.MEDIA_URL
    except:
        pass


    # generate form context
    about_file = File(open(os.path.join(_file_path, 'about_me.txt')))
    about_code_file = File(open(os.path.join(_file_path, 'about_code.txt')))
    about_motorcycle_file = File(open(os.path.join(_file_path, 'about_motorcycle.txt')))
    about_culture_file = File(open(os.path.join(_file_path, 'about_culture.txt')))
    contact_file = File(open(os.path.join(_file_path, 'contact.txt')))

    # get skills by each type
    skills_language = Skill.objects.get_by_type("LN")
    skills_backend = Skill.objects.get_by_type("BE")
    skills_frontend = Skill.objects.get_by_type("FE")
    skills_db = Skill.objects.get_by_type("DB")
    skills_method = Skill.objects.get_by_type("MT")
    skills_tech = Skill.objects.get_by_type("TE")

    # get projects
    projects = Project.objects.get_all()

    context = {
        "about_file": about_file,
        "about_code_file": about_code_file,
        "about_motorcycle_file": about_motorcycle_file,
        "about_culture_file": about_culture_file,
        "contact_file": contact_file,
        "skills_language": skills_language,
        "skills_backend": skills_backend,
        "skills_frontend": skills_frontend,
        "skills_db": skills_db,
        "skills_method": skills_method,
        "skills_tech": skills_tech,
        "projects": projects
    }
    return render(request, "main/base.html", context)


def filter_project(request, language):
    if language == "csharp": language = "c#"
    if language == "all":
        projects = Project.objects.all()
    else:
        try:
            lang_instance = Skill.objects.get(
                skill_name__iexact=language
                )
        except ObjectDoesNotExist:
            raise Http404("Language does not exist.")
        projects = Project.objects.filter(skills__id=lang_instance.id)
    context = {
        'projects': projects
    }
    html = render_to_string('main/projects.html', context, request)
    return HttpResponse(html)


def get_project(request, id):
    project = get_object_or_404(Project, id=id)
    images = ProjectImage.objects.filter(project=id)
    context = {
        'project': project,
        'images': images
    }
    html = render_to_string("main/project_modal.html", context, request)
    return HttpResponse(html)

def recaptcha_check(request):
    # verify whether the recaptcha check passed successfully
    # through the Google ReCaptcha API
    # secret is different from the sitekey on the template
    # response is the data returned by the recaptcha widget
    recaptcha_params = {
        'secret': "6LdegUAUAAAAACWNaIay-1bhBUrreVHuZRoGZc_0",
        'response': request.body
    }
    recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"

    r = requests.get(recaptcha_url, params=recaptcha_params)
    r = r.json()
    try:
        if(r['success']):
            # the recaptcha succeeded, store in session for future use
            request.session['recaptcha'] = request.body
            # add the e-mail modal to the page
            # include the email messaging form
            # include the recaptcha response in the form
            form = NewMessageForm()
            context = {
                'form': form,
                'recaptcha': recaptcha_params['response']
            }
            html = render_to_string("main/email_safe.html", context, request)
        else:
            # the recaptcha failed
            # do not add the e-mail to the page
            html = render_to_string("main/email_error.html")
    except:
        # there was an error in the API call
        # do not add the e-mail to the page
        html = render_to_string("main/email_error.html")
    return HttpResponse(html)


# this helper function evaluates the httprequest
# so that it can be viewed as a human-friendly message
def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize()
                           for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
    )


def send_message(request):
    # transform form data to json
    form_json = json.loads(request.body)
    # setup partial template addresses
    render_error_partial = "main/email_form.html"
    render_success_partial = "main/email_sent.html"

    # prior to validating email, confirm user passed recaptcha
    if 'recaptcha' in request.session and request.session['recaptcha'] == form_json['recaptcha']:
        # use forms.py to validate form data
        form = NewMessageForm(form_json)
        if form.is_valid():
            # form data is valid
            my_email = DEFAULT_FROM_EMAIL
            email = Message.objects.create(
                sender_name=form_json['sender_name'],
                sender_email=form_json['sender_email'],
                subject=form_json['subject'],
                message_text=form_json['message_text']
            )
            # send message and automatically reply to user
            email_subject = "[Portfolio Website] " + email.subject
            email_subject += " -- FROM " + email.sender_name
            email_subject += " (" + email.sender_email + ")"
            email_content = "Message From: " + email.sender_name + "\n"
            email_content += "Sender Email: " + email.sender_email + "\n\n"
            email_content += email.message_text
            try:
                send_mail(
                    subject=email_subject,
                    message=email_content, 
                    from_email=my_email,
                    recipient_list=[my_email]
                )

                reply_subject = "Thank You for Your Message!"
                reply_template = get_template('email/template.txt')
                reply_context = {
                    'sender_name': email.sender_name,
                    'sender_email': email.sender_email,
                    'subject': email.subject,
                    'message_sent': email.message_sent,
                    'message_text': email.message_text
                }
                reply_content = reply_template.render(reply_context)
                send_mail(
                    subject=reply_subject,
                    message=reply_content,
                    from_email=my_email,
                    recipient_list=[email.sender_email]
                )

                # generate modal html string to tell user message sent
                context = {
                    'email': email
                }
                html = render_to_string(render_success_partial, context)
                # header to tell client javascript how to handle the response
                _header_value = "True"

            except BadHeaderError:
                html = "<h3>Invalid header found.</h3><p>You must refresh the page in order to use this contact feature again.</p>"
                # header to tell client javascript how to handle the response
                _header_value = "True"

        else:
            # form data is not valid
            # render the form partial with errors and request
            context = {
                'form': form,
                'recaptcha': form_json['recaptcha']
            }

            # regenerate form modal html string to display errors
            html = render_to_string(render_error_partial, context, request)
            # header to tell client javascript how to handle the response
            _header_value = "False"
    else:
        # the user did not pass recaptcha
        html = render_to_string("main/email_error.html")
        _header_value = "False"

    # return success or error html partial with custom header
    _xheader = "Response-Email-Sent"
    _http_response = HttpResponse(html)
    _http_response.__setitem__(_xheader, _header_value)
    return _http_response

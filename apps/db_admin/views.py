# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# local app-specific imports
from django.shortcuts import render, redirect
from django.urls import reverse

# import forms and related modules
from django import forms
from django.forms.utils import ErrorList
from django.contrib import messages
# from ..main.exceptions import admin_user_confirm, const
# from django.shortcuts import get_object_or_404

# import related models
# from django.contrib import auth
# from .models import User


# def construct_session_context(request):
#     # use this function to construct the logged in user context
#     context = {}
#     if 'user_id' in request.session:
#         context = {
#             "username": request.session['username'],
#             "user_first": request.session['user_first']
#         }
#     return context


# def admin_access_denied(request):
#     return redirect(reverse('home'))


# def admin_index(request):
#     # check if the user previously submitted a form with errors
#     if 'form_values' in request.session:
#         # create a new form instance with the values stored in session
#         # form = NewAdminForm(request.session['form_values'])

#         # create errors to view on the template
#         # form.is_valid()
#         del request.session['form_values']
#     # else:
#         # form = NewAdminForm()
#     user = construct_session_context(request)
#     # return render(request, 'db_admin/index.html', {'form': form, 'user': user})
#     return


# def admin_login(request):
#     username = request.POST.get('username', '')
#     password = request.POST.get('password', '')
#     user = auth.authenticate(username=username, password=password)
#     if user is not None and user.is_active:
#         # correct password, and the user is marked "active"
#         auth.login(request, user)
#         request.session['user_id'] = user['id']
#         request.session['username'] = user['username']
#         request.session['user_first'] = user['first_name']
#         return redirect(reverse('db_admin', 'skills'))
#     else:
#         # show an error page
#         return redirect(reverse('login'))

#     # result = User.objects.login_validator(request, request.POST)
#     # result is a dictionary object with errors and user, if successful
#     # errors = result['errors']
#     # if len(errors):
#     #     # the validator returned errors
#     #     for err in errors:
#     #         extra_tags = err['tag']
#     #         messages.error(request, err['message'], extra_tags=extra_tags)
#     #     return redirect('/admin')
#     # else:
#     #     # no errors, login and proceed to first page
#     #     user = result['user']
#     #     request.session['user_id'] = user['id']
#     #     request.session['username'] = user['username']
#     #     request.session['user_first'] = user['first_name']
#     #     first_page = '/admin/skill/index'
#     #     return redirect(first_page)


# def admin_logout(request):
#     if not request.user.is_authenticated():
#         # if not admin_user_confirm(request):
#         return redirect(const.redirect_403)
#     try:
#         auth.logout(request)
#         # del request.session['user_id']
#         # del request.session['username']
#         # del request.session['user_first']
#     except KeyError:
#         pass
#     return redirect(reverse('home'))


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
        



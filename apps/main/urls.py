from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^project/filter/(?P<language>[a-z]+)$',
        views.filter_project, name="filter_project"),
    url(r'^project/(?P<id>[0-9]+)$',
        views.get_project, name="get_project"),

    url(r'^email$', views.recaptcha_check, name="msg_recaptcha"),
    url(r'^email/send_msg$', views.send_message, name="msg_send"),

    url(r'^click/admin/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_admin"),
    url(r'^click/contact/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_contact"),
    url(r'^click/header/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_header"),
    url(r'^click/login/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_login"),
    url(r'^click/navbar/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_navbar"),
    url(r'^click/project/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_project"),
    url(r'^click/resume/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_resume"),
    url(r'^click/skill/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_skill"),
    url(r'^hover/(?P<address>[-!@#$%&\w\s]+)$', views.record_click, name="record_hover"),

    url(r'^accounts/guest/', views.get_guest_login, name="get_guest_login"),

    url(r'^', views.main_page, name="home"),
]

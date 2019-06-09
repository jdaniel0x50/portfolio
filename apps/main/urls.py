from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^project/filter/(?P<language>[a-z]+)$',
        views.filter_project, name="filter_project"),
    re_path(r'^project/(?P<id>[0-9]+)$',
        views.get_project, name="get_project"),

    re_path(r'^email$', views.recaptcha_check, name="msg_recaptcha"),
    re_path(r'^email/send_msg$', views.send_message, name="msg_send"),

    re_path(r'^click/admin/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_admin"),
    re_path(r'^click/contact/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_contact"),
    re_path(r'^click/header/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_header"),
    re_path(r'^click/login/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_login"),
    re_path(r'^click/navbar/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_navbar"),
    re_path(r'^click/project/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_project"),
    re_path(r'^click/resume/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_resume"),
    re_path(r'^click/skill/(?P<address>[-a-zA-Z]+)$', views.record_click, name="click_skill"),
    re_path(r'^hover/(?P<address>[-!@#$%&\w\s]+)$', views.record_click, name="record_hover"),

    re_path(r'^accounts/guest/', views.get_guest_login, name="get_guest_login"),

    re_path(r'^', views.main_page, name="home"),
]

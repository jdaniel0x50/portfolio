from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'(.*).css', views.serve, name="styles"),
    url(r'^project/filter/(?P<language>[a-z]+)$',
        views.filter_project, name="filter_project"),
    url(r'^project/(?P<id>[0-9]+)$',
        views.get_project, name="get_project"),
    url(r'^email$', views.recaptcha_check, name="msg_recaptcha"),
    url(r'^email/send_msg$', views.send_message, name="msg_send"),
    url(r'^$', views.main_page, name="home"),
    url(r'^/$', views.main_page, name="home_alt"),

]

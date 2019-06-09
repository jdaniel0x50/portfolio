"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.http import HttpResponse
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
admin.autodiscover()


urlpatterns = [
    re_path(r'robots.txt$', lambda x: HttpResponse("User-Agent: *\nAllow: /$\nDisallow: /", content_type="text/plain"), name="robots_file"),
    re_path(r'^admin/main/', include(('apps.db_admin.urls', 'db_admin'), namespace='db_admin')),
    # url(r'^admin/', include(admin.site.urls)),
    re_path(r'^admin/', RedirectView.as_view(pattern_name='login', permanent=False)),
    re_path(r'^accounts/login/', LoginView.as_view(template_name='db_admin/login.html'), name='login'),
    re_path(r'^accounts/logout/', LogoutView.as_view(template_name='db_admin/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

urlpatterns.append(re_path(r'^', include(('apps.main.urls', 'main'), namespace="home")))

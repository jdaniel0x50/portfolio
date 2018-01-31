from django.conf.urls import url
from django.contrib import admin

from . import views as AdminViews
from ..main import views as MainViews
from ._projects import views as ProjectViews

urlpatterns = [
    # login routes
    url(r'^login', AdminViews.admin_login),
    # url(r'^register', AdminViews.create_admin),
    url(r'^access_denied', AdminViews.admin_access_denied),
    url(r'^logout', AdminViews.admin_logout),
    # url(r'^all$', AdminViews.admin_show_all),
    # url(r'^(?P<id>[0-9]+)$', AdminViews.read_admin),
    # url(r'^(?P<id>[0-9]+)/edit$', AdminViews.edit_admin_page),
    # url(r'^(?P<id>[0-9]+)/edit/update$', AdminViews.update_admin),
    # url(r'^(?P<id>[0-9]+)/destroy$', AdminViews.destroy_admin),

    # skill routes
    url(r'^skill/index$', AdminViews.skills_index),
    url(r'^skill/index/sort=(?P<sort_f>[a-zA-Z_\-]+)', AdminViews.skills_index),
    url(r'^skill/create', AdminViews.skills_create),
    url(r'^skill/edit/(!P<id>[0-9]+)', AdminViews.skills_index),
    url(r'^skill/destroy/(!P<id>[0-9]+)', AdminViews.skills_index),

    # project routes
    url(
        r'^project/index$', 
        ProjectViews.projects_index,
        name="projects"
    ),
    url(
        r'^project/index/sort=(?P<sort_f>[a-zA-Z_\-]+)',
        ProjectViews.projects_index,
        name="projects_sort"
    ),
    url(
        r'^project/create', 
        ProjectViews.projects_create,
        name="project_create"
    ),
    url(
        r'^project/edit/(?P<id>[0-9]+)', 
        ProjectViews.project_edit,
        name="project_edit"
    ),
    url(
        r'^project/destroy/(?P<id>[0-9]+)', 
        ProjectViews.destroy_project,
        name="project_remove"
    ),
    
    # project images
    url(
        r'^project/(?P<id>[0-9]+)/image/add', 
        ProjectViews.img_upload,
        name="pimage_add"
    ),
    url(
        r'^project/(?P<id>[0-9]+)/image/get', 
        ProjectViews.img_getall,
        name="pimage_all_for_project"
    ),
    url(
        r'^project/(?P<id>[0-9]+)/image/(?P<image_id>[0-9]+)/edit', 
        ProjectViews.img_edit,
        name="pimage_get_edit"
    ),  # GET route
    url(
        r'^project/(?P<id>[0-9]+)/image/(?P<image_id>[0-9]+)/update', 
        ProjectViews.img_edit,
        name="pimage_post_update"
    ),  # POST route
    url(
        r'^project/(?P<id>[0-9]+)/image/(?P<image_id>[0-9]+)/feature',
        ProjectViews.img_mark_feature,
        name="pimage_mark_feature"
    ),  # POST route
    url(
        r'^project/(?P<id>[0-9]+)/image/(?P<image_id>[0-9]+)/remove',
        ProjectViews.destroy_image,
        name="pimage_remove"
    ),

    # message routes
    url(r'^message/index$', AdminViews.message_index),
    url(r'^message/index/sort=(?P<sort_f>[a-zA-Z_\-]+)',
        AdminViews.message_index),
    url(r'^message/destroy/(?P<id>[0-9]+)', AdminViews.destroy_message),

    # index route (at end)
    url(r'^', AdminViews.admin_index),

]

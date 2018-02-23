from django.conf.urls import url
from django.contrib import admin

from . import views as AdminViews
from ..main import views as MainViews
from ._messages import views as MessageViews
from ._projects import views as ProjectViews
from ._skills import views as SkillViews
from ._traffic import views as TrafficViews
from ._resume import views as ResumeViews

urlpatterns = [
    # login routes
    # url(r'^login', AdminViews.admin_login),
    # url(r'^register', AdminViews.create_admin),
    # url(r'^access_denied', AdminViews.admin_access_denied),
    # url(r'^logout', AdminViews.admin_logout),

    # skill routes
    url(r'^skill/$', SkillViews.skills_index, name="skills"),
    url(r'^skill/sort=(?P<sort_f>[a-zA-Z_\-]+)$',
        SkillViews.skills_index, name="skills_sort"),
    url(r'^skill/create', SkillViews.skills_create, name="skill_create"),
    url(r'^skill/(?P<id>[0-9]+)/edit$',
        SkillViews.skills_index, name="skill_edit"),
    url(r'^skill/(?P<id>[0-9]+)/logo$',
        SkillViews.skill_logo, name="skill_logo"),
    url(r'^skill/(?P<id>[0-9]+)/logo/(?P<logo_id>[0-9]+)/destroy$',
        SkillViews.skill_logo_destroy, name="skill_logo_destroy"),
    url(r'^skill/(?P<id>[0-9]+)/destroy$',
        SkillViews.skill_destroy, name="skill_destroy"),

    # project routes
    url(
        r'^project/$', 
        ProjectViews.projects_index,
        name="projects"
    ),
    url(
        r'^project/sort=(?P<sort_f>[a-zA-Z_\-]+)',
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
        name="project_destroy"
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
        name="pimage_destroy"
    ),

    # message routes
    url(r'^message/$', MessageViews.message_index, name='messages'),
    url(r'^message/sort=(?P<sort_f>[a-zA-Z_\-]+)',
        MessageViews.message_index, name='messages_sort'),
    url(r'^message/(?P<id>[0-9]+)/destroy',
        MessageViews.destroy_message, name='message_destroy'),

    # resume routes
    url(r'^resume/$', ResumeViews.index, name='resume'),
    url(r'^resume/add$', ResumeViews.upload, name='resume_upload'),
    url(r'^resume/list$', ResumeViews.list, name='resume_list'),
    url(r'^resume/(?P<id>[0-9]+)/destroy$', ResumeViews.destroy, name='resume_destroy'),

    # traffic routes
    url(r'^traffic/$', TrafficViews.traffic_index, name='traffic'),
    url(r'^traffic/sort=(?P<sort_f>[a-zA-Z_\-]+)',
        TrafficViews.traffic_index, name='traffic_sort'),

]

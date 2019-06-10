from django.urls import re_path

from ._contacts import views as ContactViews
from ._messages import views as MessageViews
from ._projects import views as ProjectViews
from ._skills import views as SkillViews
from ._traffic import views as TrafficViews
from ._resume import views as ResumeViews

urlpatterns = [
    # skill routes
    re_path(r'^skill/$', SkillViews.skills_index, name="skills"),
    re_path(r'^skill/sort=(?P<sort_f>[a-zA-Z_\-]+)$',
        SkillViews.skills_index, name="skills_sort"),
    re_path(r'^skill/create', SkillViews.skills_create, name="skill_create"),
    re_path(r'^skill/(?P<id>[0-9]+)/edit$',
        SkillViews.skills_index, name="skill_edit"),
    re_path(r'^skill/(?P<id>[0-9]+)/logo$',
        SkillViews.skill_logo, name="skill_logo"),
    re_path(r'^skill/(?P<id>[0-9]+)/logo/(?P<logo_id>[0-9]+)/destroy$',
        SkillViews.skill_logo_destroy, name="skill_logo_destroy"),
    re_path(r'^skill/(?P<id>[0-9]+)/destroy$',
        SkillViews.skill_destroy, name="skill_destroy"),

    # project routes
    re_path(
        r'^project/$', 
        ProjectViews.projects_index,
        name="projects"
    ),
    re_path(
        r'^project/sort=(?P<sort_f>[a-zA-Z_\-]+)',
        ProjectViews.projects_index,
        name="projects_sort"
    ),
    re_path(
        r'^project/create', 
        ProjectViews.projects_create,
        name="project_create"
    ),
    re_path(
        r'^project/edit/(?P<id>[0-9]+)', 
        ProjectViews.project_edit,
        name="project_edit"
    ),
    re_path(
        r'^project/destroy/(?P<id>[0-9]+)', 
        ProjectViews.destroy_project,
        name="project_destroy"
    ),
    
    # project images
    re_path(
        r'^project/(?P<id>[0-9]+)/image/add', 
        ProjectViews.img_upload,
        name="pimage_add"
    ),
    re_path(
        r'^project/(?P<id>[0-9]+)/image/get', 
        ProjectViews.img_getall,
        name="pimage_all_for_project"
    ),
    re_path(
        r'^project/(?P<id>[0-9]+)/image/(?P<image_id>[0-9]+)/edit', 
        ProjectViews.img_edit,
        name="pimage_get_edit"
    ),  # GET route
    re_path(
        r'^project/(?P<id>[0-9]+)/image/(?P<image_id>[0-9]+)/update', 
        ProjectViews.img_edit,
        name="pimage_post_update"
    ),  # POST route
    re_path(
        r'^project/(?P<id>[0-9]+)/image/(?P<image_id>[0-9]+)/feature',
        ProjectViews.img_mark_feature,
        name="pimage_mark_feature"
    ),  # POST route
    re_path(
        r'^project/(?P<id>[0-9]+)/image/(?P<image_id>[0-9]+)/remove',
        ProjectViews.destroy_image,
        name="pimage_destroy"
    ),

    # message routes
    re_path(r'^message/$', MessageViews.message_index, name='messages'),
    re_path(r'^message/sort=(?P<sort_f>[a-zA-Z_\-]+)',
        MessageViews.message_index, name='messages_sort'),
    re_path(r'^message/(?P<id>[0-9]+)/destroy',
        MessageViews.destroy_message, name='message_destroy'),

    # contact routes
    re_path(r'^contact/$', ContactViews.contact_index, name='contacts'),
    re_path(r'^contact/sort=(?P<sort_f>[a-zA-Z_\-]+)',
        ContactViews.contact_index, name='contacts_sort'),
    re_path(r'^contact/(?P<id>[0-9]+)/destroy',
        ContactViews.destroy_contact, name='contact_destroy'),

    # resume routes
    re_path(r'^resume/$', ResumeViews.index, name='resume'),
    re_path(r'^resume/add$', ResumeViews.upload, name='resume_upload'),
    re_path(r'^resume/list$', ResumeViews.list, name='resume_list'),
    re_path(r'^resume/(?P<id>[0-9]+)/destroy$', ResumeViews.destroy, name='resume_destroy'),

    # traffic routes
    re_path(r'^traffic/$', TrafficViews.traffic_index, name='traffic'),
    re_path(r'^traffic/sort=(?P<sort_f>[a-zA-Z_\-]+)',
        TrafficViews.traffic_index, name='traffic_sort'),

]

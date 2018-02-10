# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from portfolio.settings_environ import DOMAIN_NAME
from datetime import date, datetime, timedelta
import os


# Global Helper function to generate a case-insensitive
# sorting query (use return values with .extra() query)
def case_insensitive_criteria(sort_field, default):
    if sort_field == "none":
        sort_field = default
    if sort_field[0] == '-':
        order_field = '-lower_field'
    else:
        order_field = 'lower_field'
    field_only = sort_field.strip('-')
    lower_field = "lower(" + field_only + ")"
    return (lower_field, order_field)


class SkillManager(models.Manager):
    def get_all(self, sort_field="none", default="skill_name"):
        # get variables to generate case-insensitive sort query
        lower_field, order_field = case_insensitive_criteria(
            sort_field, default
        )
        skills = (Skill.objects.all()
            .extra(select={'lower_field':lower_field})
            .order_by(order_field))
        return skills

    def get_by_type(self, type):
        skills = Skill.objects.filter(skill_type=type)
        return skills

    def all_choices(self, sort_field="none", default="skill_name"):
        # get variables to generate case-insensitive sort query
        lower_field, order_field = case_insensitive_criteria(
            sort_field, default
        )
        skills = (Skill.objects.all()
            .extra(select={'lower_field':lower_field})
            .order_by(order_field)
        )
        choices = ()
        # for choice in skills:
        #     skill_string = choice.skill_name + " [" + choice.skill_type + "]"
        #     choices = choices + ((choice.id, skill_string),)
        return choices

    def get_total(self):
        totals = {}
        totals['total'] = Skill.objects.all().count()
        for key, value in Skill.SkillTypeChoices.SKILL_TYPE_CHOICES:
            _count = Skill.objects.filter(skill_type=key).count()
            totals[key] = _count
        return totals


class MessageManager(models.Manager):
    def get_all(self, sort_field="none", default="-message_sent"):
        lower_field, order_field = case_insensitive_criteria(
            sort_field, default
        )
        messages = (Message.objects.all()
                    .extra(select={'lower_field':lower_field})
                    .order_by(order_field))
        return messages

    def get_total(self):
        totals = {}
        totals['total'] = Message.objects.all().count()
        totals['1day'] = Message.objects.filter(
            message_sent__gte=datetime.now() - timedelta(days=1)).count()
        totals['1week'] = Message.objects.exclude(
            message_sent__gte=datetime.now() - timedelta(days=1)).filter(
            message_sent__gte=datetime.now() - timedelta(days=7)).count()
        totals['2week'] = Message.objects.exclude(
            message_sent__gte=datetime.now() - timedelta(days=7)).filter(
            message_sent__gte=datetime.now() - timedelta(days=14)).count()
        totals['1month'] = Message.objects.filter(
            message_sent__gte=datetime.now() - timedelta(weeks=4)).count()
        totals['2month'] = Message.objects.exclude(
            message_sent__gte=datetime.now() - timedelta(weeks=4)).filter(
            message_sent__gte=datetime.now() - timedelta(weeks=8)).count()
        return totals


class ProjectManager(models.Manager):
    def get_all(self, sort_field="none", default="feat_order"):
        if sort_field == "none" or sort_field == "feat_order":
            projects = Project.objects.all().order_by("feat_order")
        else:
            lower_field, order_field = case_insensitive_criteria(
                sort_field, default
            )
            projects = (Project.objects.all()
                        .extra(select={'lower_field':lower_field})
                        .order_by(order_field))
        return projects
    
    def filter_language(self, language):
        projects = Project.objects.filter(skills_skill_name__iexact=language)
        return projects

    def get_total(self):
        totals = {}
        # totals['total'] = Message.objects.all().count()
        # totals['1day'] = Message.objects.filter(
        #     message_sent__gte=datetime.now() - timedelta(days=1)).count()
        # totals['1week'] = Message.objects.exclude(
        #     message_sent__gte=datetime.now() - timedelta(days=1)).filter(
        #     message_sent__gte=datetime.now() - timedelta(days=7)).count()
        # totals['2week'] = Message.objects.exclude(
        #     message_sent__gte=datetime.now() - timedelta(days=7)).filter(
        #     message_sent__gte=datetime.now() - timedelta(days=14)).count()
        # totals['1month'] = Message.objects.filter(
        #     message_sent__gte=datetime.now() - timedelta(weeks=4)).count()
        # totals['2month'] = Message.objects.exclude(
        #     message_sent__gte=datetime.now() - timedelta(weeks=4)).filter(
        #     message_sent__gte=datetime.now() - timedelta(weeks=8)).count()
        return totals

class ProjectImageManager(models.Manager):
    def get_all_images(self):
        images = ProjectImage.objects.all().order_by('order')
        return images

    def get_all_project(self, project_id):
        images = ProjectImage.objects.filter(project=project_id).order_by('order')
        return images

    def remove(self, id):
        print "**** Inside remove!"
        pimage = ProjectImage.objects.get(id=id)
        proj = Project.objects.get(id=pimage.project.id)
        print "**** Got Project!"
        # print "Project featured image: " + proj.featimage_url
        # if proj.featimage_url == pimage.img_url:
            # print "they are the same"


class Skill(models.Model):
    # Encapsulate the skill type choices within the skill model
    class SkillTypeChoices(models.Model):
        LANGUAGE = 'LN'
        BACK_END_FRAMEWORK = 'BE'
        FRONT_END_FRAMEWORK = 'FE'
        DATABASE = 'DB'
        METHODOLOGY = 'MT'
        TECHNOLOGY = 'TE'
        SKILL_TYPE_CHOICES = (
            (LANGUAGE, 'Language'),
            (BACK_END_FRAMEWORK, 'Back End Framework'),
            (FRONT_END_FRAMEWORK, 'Front End Framework'),
            (DATABASE, 'Database'),
            (METHODOLOGY, 'Methodology'),
            (TECHNOLOGY, 'Technology/Tool')
        )

    skill_name = models.CharField(max_length=200)
    skill_type = models.CharField(
        max_length=2,
        choices=SkillTypeChoices.SKILL_TYPE_CHOICES
    )
    logo_url = models.CharField(max_length=255)
    skill_level = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SkillManager()


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    subtitle = models.CharField(
        max_length=255,
        blank=True,
    )
    description = models.TextField()
    impact = models.CharField(
        max_length=255,
        blank=True
    )
    deploy_url = models.CharField(
        max_length=255,
        blank=True,
    )
    code_url = models.CharField(
        max_length=255,
        blank=True,
    )
    featimage_url = models.CharField(
        max_length=255,
        blank=True,
    )
    feat_order = models.SmallIntegerField(
        default=99
    )
    video_url = models.CharField(
        max_length=255,
        blank=True,
    )
    skills = models.ManyToManyField(
        Skill,
        related_name='ProjectSkills'
    )
    project_timeline = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectManager()


def img_directory_path(instance, filename):
    # generate image upload path
    # file will be uploaded to MEDIA_ROOT/project/<id>/<filename>
    return 'project/{0}/{1}'.format(instance.project.id, filename)

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    img_url = models.ImageField(upload_to=img_directory_path)
    caption = models.CharField(max_length=255, blank=True)
    order = models.SmallIntegerField(default=9)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectImageManager()

    def print_stuff(self):
        # print self.img_url.upload_to
        print self.img_url.storage
        print self.img_url.path
        # print self.img_url.get_filename

    def filename(self):
        return os.path.basename(self.img_url.name)

    def delete(self):
        # storage, path = self.img_url.storage, self.img_url.path
        # storage.delete(path)

        # compare to project featured image
        p = Project.objects.get(id=self.project)
        f_img = p.featimage_url
        print "Project feature image: ", f_img
        print "Image URL: ", self.img_url.url
        if self.img_url.url == f_img:
            p.featimage_url = ""
            p.save()
        self.img_url.delete(save=False)
        super(ProjectImage, self).delete()


class Message(models.Model):
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField(max_length=100)
    subject = models.CharField(
        max_length=100,
        default="FollowUp to " + DOMAIN_NAME
    )
    message_text = models.TextField()
    message_sent = models.DateTimeField(auto_now=True)
    objects = MessageManager()


    
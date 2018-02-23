# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import os


class ResumeManager(models.Manager):
    def most_recent(self):
        return Resume.objects.latest()

    def get_all(self):
        return Resume.objects.all().order_by('-created_at')


def resume_directory_path(instance, filename):
    # generate file upload path
    # file will be uploaded to MEDIA_ROOT/resume/<filename>
    return 'resume/{0}/{1}'.format(instance.id, filename)


class Resume(models.Model):
    res_file = models.FileField(
        upload_to=resume_directory_path
    )
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ResumeManager()

    class Meta:
        get_latest_by = 'created_at'

    def filename(self):
        return os.path.basename(self.res_file.name)

    def delete(self):
        self.res_file.delete(save=False)
        super(Resume, self).delete()


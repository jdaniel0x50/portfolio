from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from ...main.models import Skill, Project, ProjectImage
from datetime import date, datetime


def today_as_string():
    today = date.today().isoformat()
    return today


class NewProjectForm(forms.Form):
    project_name = forms.CharField(
        label="Project",
        max_length=100,
        required=True,
        strip=True,
    )
    subtitle = forms.CharField(
        label="Subtitle",
        max_length=255,
        required=False,
        strip=True
    )
    description = forms.CharField(
        label="Description",
        max_length=1000,
        required=True,
        strip=True,
        widget=forms.Textarea
    )
    impact = forms.CharField(
        label="Impact",
        max_length=255,
        required=False,
        strip=True
    )
    project_timeline = forms.DateField(
        label="Date",
        help_text="Approximate dates are fine. Dates will displayed roughly as month year",
        initial=today_as_string(),
        input_formats=['%Y-%m-%d',      # '2006-10-25'
                       '%m/%d/%Y',      # '10/25/2006'
                       '%m/%d/%y']      # '10/25/06'
    )
    deploy_url = forms.CharField(
        label="Web URL",
        max_length=255,
        required=False,
        strip=True
    )
    code_url = forms.CharField(
        label="Code URL",
        max_length=255,
        required=False,
        strip=True
    )
    # featimage_url = forms.CharField(
    #     label="Feature Image",
    #     required=False,
    #     max_length=255,
    #     strip=True,
    #     validators=[
    #         RegexValidator(
    #             regex=r'^project/img/[a-zA-Z0-9_\-\.]+',
    #             message="Invalid format"
    #         )
    #     ]
    # )
    feat_order = forms.IntegerField(
        label="Feature Order",
        min_value=0,
        initial=99,
        help_text="Projects will appear on the page in order, from lower to higher values"
    )
    # video_url = forms.CharField(
    #     label="Video URL",
    #     required=False,
    #     max_length=255,
    #     strip=True,
    #     validators=[
    #         RegexValidator(
    #             regex=r'^project/video/[a-zA-Z0-9_\-\.]+',
    #             message="Invalid format"
    #         )
    #     ]
    # )
    skills = forms.MultipleChoiceField(
        label="Skills",
        choices=(Skill.objects.all_choices())
    )

class NewImageForm(forms.ModelForm):
    class Meta:
        model=ProjectImage
        fields=('project', 'caption', 'order', 'img_url')

class EditImageForm(forms.ModelForm):
    class Meta:
        model=ProjectImage
        fields=('project', 'caption', 'order')

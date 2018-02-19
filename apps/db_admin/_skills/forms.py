from django import forms
from django.core.validators import RegexValidator
from ...main.models import Skill, SkillImage


class NewSkillForm(forms.Form):
    skill_name = forms.CharField(
        label="Skill",
        max_length=200,
        required=True,
        strip=True,
        validators=[
            RegexValidator(
                regex='[a-zA-Z0-9@#_\-\.\s\(\)]+',
                message="Invalid format"
            ),
        ]
    )
    skill_type = forms.ChoiceField(
        label="Type",
        required=True,
        choices=(Skill.SkillTypeChoices.SKILL_TYPE_CHOICES),
        widget=forms.Select()
    )
    logo_url = forms.CharField(
        label="Logo URL",
        required=True,
        max_length=255,
        strip=True,
        validators=[
            RegexValidator(
                regex=r'^base/img/logos/[a-zA-Z0-9_\-\.]+',
                message="Invalid format"
            )
        ]
    )
    skill_level = forms.IntegerField(
        label="Skill Level",
        required=True,
        min_value=1,
        max_value=5,
        initial=4
    )


class NewSkillImageForm(forms.ModelForm):
    class Meta:
        model=SkillImage
        fields=('skill', 'img')

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from .models import User, UserManager
from ..main.models import Skill, Project


PASSWORD_REGEX = re.compile(r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[\w\d!@#$%^&?._]{8,15}$')

class NewAdminForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=True,
        min_length=2,
        max_length=50,
        strip=True,
        validators=[
            RegexValidator(
                regex='[a-zA-Z0-9@_\-\.]+',
                message='Usernames may contain letters, numbers, ampersand, hyphen, underscore, and periods (no spaces)'
            ),
        ]
    )
    first_name = forms.CharField(
        label="First Name",
        required=True,
        min_length=1,
        max_length=50,
        strip=True,
        validators=[
            RegexValidator(
                regex='[a-zA-Z\s\.]+',
                message='Names may contain letters, spaces, and periods'
            ),
        ]
    )
    last_name = forms.CharField(
        label="Last Name",
        required=True,
        min_length=1,
        max_length=50,
        strip=True,
        validators=[
            RegexValidator(
                regex='[a-zA-Z\s\.]+',
                message='Names may contain letters, spaces, and periods'
            ),
        ]
    )
    password = forms.CharField(
        label="Password",
        required=True,
        min_length=8,
        max_length=15,
        widget=forms.PasswordInput(render_value=True),
        validators=[
            RegexValidator(
                regex=PASSWORD_REGEX,
                message='Password must contain at least one digit, lower case letter, and upper case letter; special characters are optional'
            )
        ]
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(render_value=False)
    )

    def clean_username(self):
        # override the clean method on the username field
        cleaned_data = self.cleaned_data['username']

        # verify the username is unique
        if not User.objects.unique_validator("username", cleaned_data):
            # unique validator returned False -- not unique
            self._errors['username'] = self._errors.get('username', [])
            self._errors['username'].append(
                "Username is currently in use. Please choose another."
            )
        return cleaned_data

    def clean(self):
        # override the clean method on the form
        cleaned_data = super(NewAdminForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # verify the password and confirm password match
        if password != password_confirm:
            raise forms.ValidationError(
                "Password and Confirmation do not match",
                code="password_confirm"
            )
        return cleaned_data

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

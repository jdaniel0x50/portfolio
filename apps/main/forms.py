from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
import re
from .models import Message
from portfolio.settings_sensitive import DOMAIN_NAME

class NewMessageForm(forms.Form):
    sender_name = forms.CharField(
        label="Your Name",
        required=True,
        min_length=2,
        max_length=100,
        strip=True,
        validators=[
            RegexValidator(
                regex='[a-zA-Z\-\s\.]+',
                message='Names may contain letters, spaces, hyphen, underscore, and periods'
            ),
        ]
    )
    sender_email = forms.EmailField(
        label="Your Email",
        required=True,
        min_length=4,
        max_length=100,
        validators=[
            EmailValidator()
        ]
    )
    subject = forms.CharField(
        label="Subject",
        required=True,
        min_length=2,
        max_length=100,
        initial="Followup to " + DOMAIN_NAME,
        strip=True
    )
    message_text = forms.CharField(
        label="Message",
        required=True,
        min_length=10,
        max_length=1500,
        strip=True,
    )


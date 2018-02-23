from django import forms
from .models import Resume


class UploadResumeForm(forms.ModelForm):
    class Meta:
        model=Resume
        fields=('res_file')

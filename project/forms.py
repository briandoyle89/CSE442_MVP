from django import forms
from .models import file

class FileForm(forms.ModelForm):
    class Meta:
        model = file
        fields = ('file_name', 'course', 'file_link')
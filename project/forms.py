from django import forms
from .models import file, User, course
#To create the format for uploading files.
class FileForm(forms.ModelForm):
    #
    # def __init__(self, *args, **kwargs):
    #     this_user = kwargs.pop('this_user')
    #     super(FileForm, self).__init__(self, **kwargs)
    #     self.fields['this_user'].widget = forms.TextInput(attrs={'username': this_user})
    class Meta:
        model = file
        fields = ('file_name', 'course', 'file_link')

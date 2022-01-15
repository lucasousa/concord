from django import forms
from .models import User


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["name", "username", "image"]


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['username'].required = False


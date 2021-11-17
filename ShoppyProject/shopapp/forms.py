from django.contrib.auth.models import User
from .models import *

from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta():
        model = UserProfileRegistrationModel
        fields = ('first_name', 'last_name','username','email','password','mobilno',)
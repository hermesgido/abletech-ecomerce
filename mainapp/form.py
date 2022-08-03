from django import forms
from . models import *


class UserRegForm(forms.ModelForm):
    

    class Meta:
        

        model = User
        fields = ('username', 'email', 'password',)

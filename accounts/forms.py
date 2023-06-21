from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1')
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':('User Name')})
        self.fields['email'].widget.attrs.update({'placeholder':('Email Address')})
        self.fields['password1'].widget.attrs.update({'placeholder':('Password')})        
        del self.fields['password2']
        

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

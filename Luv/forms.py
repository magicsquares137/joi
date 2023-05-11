from django import forms
from .models import User_Posts
import yaml
import os
from django.conf import settings


with open(os.path.join(settings.BASE_DIR, 'config.yml'), 'r') as file:
	CONFIG = yaml.safe_load(file)

class NewUserRequest(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=CONFIG['MODEL_SETTINGS']['User_Posts']['message_length'])

    class Meta:
        model = User_Posts
        fields = ['message']
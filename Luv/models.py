import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import yaml


with open(os.path.join(settings.BASE_DIR, 'config.yml'), 'r') as file:
	CONFIG = yaml.safe_load(file)

class Characters(models.Model):
	name = models.CharField(max_length=CONFIG['MODEL_SETTINGS']['Characters']['name_length'], unique=True)
	description = models.CharField(max_length=CONFIG['MODEL_SETTINGS']['Characters']['description_length'])
	views = models.PositiveIntegerField(default=0)
	main_Img = models.ImageField(upload_to='img/')

	class Meta:
		verbose_name_plural = 'Characters'

	def __str__(self):
		return self.name

class User_Posts(models.Model):
	message = models.TextField(max_length=CONFIG['MODEL_SETTINGS']['User_Posts']['message_length'])
	post_date = models.DateTimeField(auto_now_add=True)
	character = models.ForeignKey(Characters, related_name='user_posts', on_delete=models.CASCADE)
	created_by = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
	non_bot = models.CharField(max_length = 10, default = 'user')
	class Meta:
		verbose_name_plural = 'User_Posts'
	def __str__(self):
		return str(self.post_date)

class Bot_Replies(models.Model):
	message = models.TextField(max_length=CONFIG['MODEL_SETTINGS']['Bot_Replies']['message_length'])
	character = models.ForeignKey(Characters, related_name='bot_posts', on_delete=models.CASCADE)
	post_date = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, related_name='user_origin', on_delete=models.CASCADE)
	non_bot = models.CharField(max_length = 10, default = 'bot')
	class Meta:
		verbose_name_plural = 'Bot_Replies'
	def __str__(self):
		return str(self.post_date)
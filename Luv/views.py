from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Characters, Bot_Replies, User_Posts
from .forms import NewUserRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from itertools import chain
import yaml
import os
from django.conf import settings

with open(os.path.join(settings.BASE_DIR, 'config.yml'), 'r') as file:
	CONFIG = yaml.safe_load(file)

# Create your views here.
def home(request):
	characters = Characters.objects.all()
	return render(request, 'home.html', {'characters': characters})

@login_required
def character_conversation(request, pk):
	character = get_object_or_404(Characters, pk = pk)
	#get most 5 recent user posts
	character.views += 1
	character.save()
	user_posts = User_Posts.objects.filter(created_by = request.user, character__pk = pk)
	bot_posts = Bot_Replies.objects.filter(created_by = request.user, character__pk = pk)
	posts_list = sorted(
		chain(user_posts, bot_posts),
		key = lambda x: x.post_date, reverse = False
		)[-CONFIG['VIEW_SETTINGS']['Message_History']:]


	if request.method == 'POST':
		form = NewUserRequest(request.POST)
		if form.is_valid():
			char_convo = form.save(commit=False)
			char_convo.message = form.cleaned_data.get('message')
			char_convo.character = character
			char_convo.created_by = request.user
			char_convo.save()
			#make api call to llm
			message = 'hello'
			#persist response to db
			#create new bot reply object
			reply = Bot_Replies(message = message, character = character, created_by = request.user).save()
			return redirect('characters', pk = character.pk)
	else:
		form = NewUserRequest()

	return render(request, 'characters_convo.html', {'character': character, 'form': NewUserRequest, 'posts': posts_list})
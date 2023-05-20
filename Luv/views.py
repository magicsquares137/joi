from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Characters, Bot_Replies, User_Posts
from .forms import NewUserRequest, Bot_Feedback
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from itertools import chain
import yaml
import os
from django.conf import settings

with open(os.path.join(settings.BASE_DIR, 'config.yml'), 'r') as file:
	CONFIG = yaml.safe_load(file)

def home(request):
	characters = Characters.objects.all()
	return render(request, 'home.html', {'characters': characters})

@login_required
def character_conversation(request, pk):
	#will need to pass user messages through pk into model api
	if request.method == 'POST' and request.POST.get("form_type") == 'user_entry':
			message = 'hello'
			character = get_object_or_404(Characters, pk = pk)
			reply = Bot_Replies(message = message, character = character, created_by = request.user).save()
	
			character.views += 1
			character.save()
	character = get_object_or_404(Characters, pk = pk)
	user_posts = User_Posts.objects.filter(created_by = request.user, character__pk = pk)
	bot_posts = Bot_Replies.objects.filter(created_by = request.user, character__pk = pk)
	posts_list = sorted(
		chain(user_posts, bot_posts),
		key = lambda x: x.post_date, reverse = False
		)[-CONFIG['VIEW_SETTINGS']['Message_History']:]


	if request.method == 'POST':
		if request.POST.get("form_type") == 'user_entry':
			form = NewUserRequest(request.POST)
			if form.is_valid():
				char_convo = form.save(commit=False)
				char_convo.message = form.cleaned_data.get('message')
				char_convo.character = character
				char_convo.created_by = request.user
				char_convo.save()
				return redirect('characters', pk = character.pk)
			else:
				form = NewUserRequest()
		if request.POST.get("form_type") == 'bot_rating':
			#instance = get_object_or_404(Bot_Replies, pk = bot_message_pk)
			form = Bot_Feedback(request.POST)#, instance = instance)
			if form.is_valid():
				rating = form.save(commit=False)
				rating.response_rating = form.cleaned_data.get('response_rating')
				#rating.save()
				return redirect('characters', pk = character.pk)
			else:
				form = Bot_Feedback()
	else:
		message_form = NewUserRequest()
		bot_rating_form = Bot_Feedback()
	return render(request, 'characters_convo.html', {'character': character, 'message_form': message_form, 'bot_rating_form': bot_rating_form, 'posts': posts_list})
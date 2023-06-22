from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .models import Characters, Bot_Replies, User_Posts, Categories, Profile
from .forms import NewUserRequest, Bot_Feedback
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from itertools import chain
import yaml
import os
from django.conf import settings
from .serializers import CharactersSerializer, UserPostsSerializer, BotRepliesSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout



with open(os.path.join(settings.BASE_DIR, "config.yml"), "r") as file:
    CONFIG = yaml.safe_load(file)


def home(request):
    characters = Characters.objects.all()
    categories = Categories.get_all_categories()
    data = {
        "categories": categories,
        "characters": characters
    }
    return render(request, "home.html", {"data": data})


class search_characters(APIView):

    def get(self,request):
        characters = Characters.objects.all()
        search_filter = request.query_params['search']
        if filter:
            characters = characters.filter(name=search_filter)
        categories = Categories.get_all_categories()
        data = {
            "categories": categories,
            "characters": characters
        }
        return render(request, "home.html", {"data": data})


class category_view(APIView):
    def get(self,request,category_id):
        characters = Characters.objects.all()
        characters = characters.filter(category_id=category_id)
        categories = Categories.get_all_categories()
        data = {
            "categories": categories,
            "characters": characters
        }
        return render(request, "home.html", {"data": data})

@method_decorator(login_required, name='dispatch')
class recent_chatpage_view(APIView):
    
    def get(self,request):
        queryset = User_Posts.objects.filter(created_by=request.user).order_by('-post_date')
        characters = [i.character for i in queryset]
        characters_unique = list(set(characters))
        # characters = characters.filter(category_id=category_id)
        categories = Categories.get_all_categories()
        data = {
            "categories": categories,
            "characters": characters_unique
        }
        return render(request, "home.html", {"data": data})


@login_required
def character_conversation(request, pk, bot_message_pk):
    # will need to pass user messages through pk into model api
    character = get_object_or_404(Characters, pk=pk)
    if request.method == "POST" and request.POST.get("form_type") == "response_rating":
        # get pk for message attached to form
        bot_message_pk = request.POST.get("form_post")
        instance = get_object_or_404(Bot_Replies, pk=bot_message_pk)
        instance.response_rating = request.POST.get("rating")
        instance.save()
        return redirect("characters", pk=character.pk, bot_message_pk=1)

    character = get_object_or_404(Characters, pk=pk)
    user_posts = User_Posts.objects.filter(created_by=request.user, character__pk=pk)
    bot_posts = Bot_Replies.objects.filter(created_by=request.user, character__pk=pk)
    profile = Profile.objects.get(user=request.user)

    if bot_posts.count() == 0:
        message = "hello"

        reply = Bot_Replies(
            message=message, character=character, created_by=request.user
        ).save()
        character.views += 1
        character.save()

    posts_list = sorted(
        chain(user_posts, bot_posts), key=lambda x: x.post_date, reverse=False
    )[-CONFIG["VIEW_SETTINGS"]["Message_History"] :]

    if request.method == "POST":
        if request.POST.get("form_type") == "user_entry":
            form = NewUserRequest(request.POST)
            if form.is_valid():
                char_convo = form.save(commit=False)
                char_convo.message = form.cleaned_data.get("message")
                char_convo.character = character
                char_convo.created_by = request.user
                char_convo.save()

                message = "hello"
                reply = Bot_Replies(
                    message=message, character=character, created_by=request.user
                ).save()
                character.views += 1
                character.save()

                return redirect(
                    "characters", pk=character.pk, bot_message_pk=bot_message_pk
                )
            else:
                message_form = NewUserRequest()
    else:
        message_form = NewUserRequest()

    return render(
        request,
        "Chat.html",
        {"profile":profile,"character": character, "message_form": NewUserRequest(), "posts": posts_list},
    )


@login_required
def update_response_rating(request, bot_message_pk):
    instance = get_object_or_404(Bot_Replies, pk=bot_message_pk)
    instance.response_rating = request.POST.get("rating")
    instance.save()
    return JsonResponse({
        "status": True,
    })


@login_required
def get_character_conversation(request, pk):
    form = NewUserRequest(request.POST)
    if form.is_valid():
        character = get_object_or_404(Characters, pk=pk)
        char_convo = form.save(commit=False)
        char_convo.message = form.cleaned_data.get("message")
        char_convo.character = character
        char_convo.created_by = request.user
        char_convo.save()

        message = "Thanks for messaging. I am under development"
        reply = Bot_Replies(
            message=message, character=character, created_by=request.user
        ).save()
        character.views += 1
        character.save()

    character = get_object_or_404(Characters, pk=pk)
    user_posts = User_Posts.objects.filter(created_by=request.user, character__pk=pk)
    bot_posts = Bot_Replies.objects.filter(created_by=request.user, character__pk=pk).order_by('-post_date')
    profile = Profile.objects.get(user=request.user)
    character_serializer = CharactersSerializer(character)
    character_data = character_serializer.data

    user_posts_serializer = UserPostsSerializer(user_posts, many=True)
    user_posts_data = user_posts_serializer.data

    if bot_posts.exists():
        latest_bot_post = bot_posts.first()
        bot_posts_serializer = BotRepliesSerializer(latest_bot_post)
        bot_posts_data = bot_posts_serializer.data
    else:
        bot_posts_data = None

    if profile.main_Img:
        profile_image = profile.main_Img.url
    else:
        profile_image = '/media/profile_images/default_user.png'


    return JsonResponse({
        "status": True,
        "character": character_data,
        "user_posts": user_posts_data[-1],
        "bot_posts": bot_posts_data,
        "user": request.user.username,
        "profile_image":profile_image
    })


class ProfileView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        profile = Profile.objects.get(user = request.user)

        context = {'profile':profile}
        return render(request, "profile.html",context)

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        username = request.POST.get('username')
        user.first_name = username

        image = request.FILES.get('image')
        if image:
            file_path = 'profile_images/' + image.name
            user.profile.main_Img.save(file_path, ContentFile(image.read()))

        user.save()

        return JsonResponse({"message":"updated Successfully"})

class DeleteUserView(LoginRequiredMixin,View):
    def post(self, request):
        if request.method == "POST":
            user = self.request.user
            user.is_active = False
            user.save()
            logout(request)
            return redirect('login')
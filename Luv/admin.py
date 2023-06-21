from django.contrib import admin
from .models import Characters, User_Posts, Bot_Replies, Profile

admin.site.register(Characters)
admin.site.register(User_Posts)
admin.site.register(Bot_Replies)
admin.site.register(Profile)

from rest_framework import serializers
from .models import Characters, User_Posts, Bot_Replies


class CharactersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characters
        fields = '__all__'

class UserPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Posts
        fields = '__all__'

class BotRepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot_Replies
        fields = '__all__'
        depth = 1

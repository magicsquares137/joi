import os
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
import yaml
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import *

with open(os.path.join(settings.BASE_DIR, "config.yml"), "r") as file:
    CONFIG = yaml.safe_load(file)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_Img = models.ImageField(upload_to="profile_images/", null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Categories(models.Model):
    name = models.CharField(
        max_length=CONFIG["MODEL_SETTINGS"]["Characters"]["name_length"], unique=True
    )
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @classmethod
    def get_all_categories(cls):
        return cls.objects.all()


class Characters(models.Model):
    name = models.CharField(
        max_length=CONFIG["MODEL_SETTINGS"]["Characters"]["name_length"], unique=True
    )
    description = models.CharField(
        max_length=CONFIG["MODEL_SETTINGS"]["Characters"]["description_length"]
    )
    views = models.PositiveIntegerField(default=0)
    main_Img = models.ImageField(upload_to="img/", validators=[validate_file_size])
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Characters"

    def __str__(self):
        return self.name


class User_Posts(models.Model):
    message = models.TextField(
        max_length=CONFIG["MODEL_SETTINGS"]["User_Posts"]["message_length"]
    )
    post_date = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(
        Characters, related_name="user_posts", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User, related_name="user_posts", on_delete=models.CASCADE
    )
    non_bot = models.CharField(max_length=10, default="user")

    class Meta:
        verbose_name_plural = "User_Posts"

    def __str__(self):
        return str(self.post_date)

class Bot_Replies(models.Model):
    message = models.TextField(
        max_length=CONFIG["MODEL_SETTINGS"]["Bot_Replies"]["message_length"]
    )
    character = models.ForeignKey(
        Characters, related_name="bot_posts", on_delete=models.CASCADE
    )
    post_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name="user_origin", on_delete=models.CASCADE
    )
    non_bot = models.CharField(max_length=10, default="bot")
    response_rating = models.CharField(max_length=4, default="Good")

    class Meta:
        verbose_name_plural = "Bot_Replies"

    def __str__(self):
        return str(self.post_date)
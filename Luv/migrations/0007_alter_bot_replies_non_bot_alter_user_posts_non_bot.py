# Generated by Django 4.2 on 2023-05-05 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Luv", "0006_bot_replies_non_bot_user_posts_non_bot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bot_replies",
            name="non_bot",
            field=models.CharField(default="user", max_length=10),
        ),
        migrations.AlterField(
            model_name="user_posts",
            name="non_bot",
            field=models.CharField(default="user", max_length=10),
        ),
    ]

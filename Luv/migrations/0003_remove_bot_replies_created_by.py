# Generated by Django 4.2 on 2023-05-03 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Luv", "0002_bot_replies_created_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bot_replies",
            name="created_by",
        ),
    ]

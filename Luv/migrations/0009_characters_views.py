# Generated by Django 4.2 on 2023-05-06 03:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Luv", "0008_alter_bot_replies_non_bot"),
    ]

    operations = [
        migrations.AddField(
            model_name="characters",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]

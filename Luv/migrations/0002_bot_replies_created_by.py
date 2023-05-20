# Generated by Django 4.2 on 2023-05-03 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Luv", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bot_replies",
            name="created_by",
            field=models.ForeignKey(
                default="temp",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_origin",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]

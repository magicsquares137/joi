from django.urls import re_path
from .views import (
    update_response_rating,
    get_character_conversation,
    ProfileView,
    DeleteUser
)

app_name = "Luv"

urlpatterns = [
    re_path(r"^update_response_rating/<int:bot_message_pk>/", update_response_rating, name="update_response_rating"),
    re_path(r"^get_character_conversation/(?P<pk>\d+)/$", get_character_conversation, name="get_character_conversation"),
    re_path(r"^account/", ProfileView.as_view(), name="account"),
    re_path(r"^delete/", DeleteUser.as_view(), name="delete_user"),
]

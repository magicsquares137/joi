from django.urls import re_path, path
from Luv.views import (
    update_response_rating,
    get_character_conversation,
    search_characters,
    category_view,
    ProfileView,
    DeleteUserView,
    recent_chatpage_view
)

app_name = "Luv"

urlpatterns = [
    re_path(r"^update_response_rating/<int:bot_message_pk>/", update_response_rating, name="update_response_rating"),
    re_path(r"^get_character_conversation/(?P<pk>\d+)/$", get_character_conversation, name="get_character_conversation"),
    re_path(r"^search/$", search_characters.as_view(), name="search"),
    path('category/<int:category_id>/', category_view.as_view(), name='category_view'),
    re_path(r"^account/", ProfileView.as_view(), name="account"),
    re_path(r"^delete/", DeleteUserView.as_view(), name="delete_user"),
    re_path(r"^chat/", recent_chatpage_view.as_view(), name="user_chats"),

]

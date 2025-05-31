from django.urls import path
from .views import chat_room, chat_room_redirect,recent_chats

app_name = "chat"

urlpatterns = [
    path("<int:room_id>/", chat_room, name="chat_room"),
    path("find/<str:user_email>/", chat_room_redirect, name="chat_room_redirect"),
    path("recent/", recent_chats, name="recent_chats"),
]

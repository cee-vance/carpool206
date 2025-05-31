import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_username = data["sender"]  # ✅ Now using username instead of email
        content = data["content"]

        sender = await get_user_by_username(sender_username)  # ✅ Changed function

        room = await get_chat_room(self.room_name)
        await save_message(room, sender, content)  # ✅ Now runs correctly

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender": sender.username,  # ✅ Changed from email to username
                "content": content,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "sender": event["sender"],
            "content": event["content"],
        }))

# ✅ Updated helper function to use username
@database_sync_to_async
def get_user_by_username(username):
    return User.objects.get(username=username)

@database_sync_to_async
def save_message(room, sender, content):
    return Message.objects.create(room=room, sender=sender, content=content)

@database_sync_to_async
def get_chat_room(chatroom_id):
    return ChatRoom.objects.get(id=chatroom_id)

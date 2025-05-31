from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class ChatRoom(models.Model):
    """Represents a chat session between users."""
    users = models.ManyToManyField(User, related_name="chat_rooms", null=True)

    def __str__(self):
        return f"Chat Room {self.id}"

class Message(models.Model):
    """Stores messages exchanged between users in a chat."""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} in Room {self.room.id}: {self.content[:30]}"

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404,redirect
from .models import ChatRoom, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models import Q

User = get_user_model()

@login_required
def chat_room(request, room_id):
    """Restrict access and load chat history."""
    chat_room = get_object_or_404(ChatRoom, id=room_id)

    # Verify user belongs to this chat room
    if request.user not in chat_room.users.all():
        return render(request, "chat/access_denied.html", {"message": "You do not have permission to access this chat."})

    # Retrieve previous messages for this chat room
    messages = Message.objects.filter(room=chat_room).order_by("timestamp")  # Ensure chronological order

    return render(request, "chat/chat_room.html", {
        "chat_room": chat_room,
        "messages": messages
    })

@login_required
def chat_room_redirect(request, user_email):
    """Find or create a chat room between the logged-in user and another user."""
    logged_in_user = request.user  # ✅ Get the CustomUser from the request
    other_user = get_object_or_404(User, email=user_email)

    # print(logged_in_user.email)
    # print(other_user.email)
    # Try to find an existing chat room
    # chat_room = ChatRoom.objects.filter(users__in=[logged_in_user, other_user]).first()

    chat_room = ChatRoom.objects.filter(users__email=logged_in_user.email).filter(users__email=other_user.email).first()


    # If no chat room exists, create one
    if not chat_room:
        chat_room = ChatRoom.objects.create()
        chat_room.users.add(logged_in_user, other_user)
        chat_room.save()

    return redirect(f"/chat/{chat_room.id}/")



@login_required
def recent_chats(request):
    """Display all chat rooms the logged-in user is part of."""
    user_chat_rooms = ChatRoom.objects.filter(users=request.user) # Sort by latest

    return render(request, "chat/recent_chats.html", {"chat_rooms": user_chat_rooms})

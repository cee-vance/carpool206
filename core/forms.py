from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django import forms

CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username","email", "password1", "password2" )#, "profile_picture", "social_links")

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login after successful signup
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

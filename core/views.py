from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required

from core.forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.decorators import login_required
from chat.models import ChatRoom

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log them in
            return redirect("core:home")  # Redirect to homepage after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, "core/register.html", {"form": form})

from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        user.profile_picture = request.FILES.get("profile_picture")
        user.social_links = request.POST.getlist("social_links")
        user.save()
        return redirect("core/profile")  # Redirect to profile page after updating
    return render(request, "core/edit_profile.html", {"user": user})



@login_required
def profile(request):
    user = request.user
    return render(request, "core/profile.html", {"user":user})


from django.contrib.auth.decorators import login_required


@login_required
def user_profile(request, email):
    """Display a user's profile and check for an existing chat room."""
    profile_user = get_object_or_404(User, email=email)

    return render(request, "core/user_profile.html", {
        "profile_user": profile_user,

    })


def landing_page(request):
    stats = {
        "carbon_goal": "90% zero-emission trips by 2030",
        "fuel_saved": "Estimated 500,000 gallons saved annually",
        "co2_reduction": "Seattle carpooling reduces CO₂ by 30% per ride"
    }
    return render(request, "core/landing.html", {"stats": stats})


@login_required()
def logout_view(request):
    """Logs out the user and redirects to the home page"""
    logout(request)  # Django’s built-in logout function
    return redirect("core:home")
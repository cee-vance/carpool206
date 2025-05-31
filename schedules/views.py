import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from carpool import settings
from .models import Schedule
from .forms import ScheduleForm
from carpool.utils import geocode_address, mins_before
from .models import Schedule
from datetime import timedelta
from math import radians, sin, cos, sqrt, atan2


User = get_user_model()
@login_required
def schedule_list(request):
    schedules = Schedule.objects.filter(user=request.user)

    # count similar schedules
    return render(request, 'schedules/schedules_list.html', {'schedules': schedules})

class ScheduleView(View):
    def get(self, request, schedule_id=None, action=None):
        """Handles showing the form for create/edit & the confirmation page for delete"""
        if action == "delete":
            schedule = get_object_or_404(Schedule, id=schedule_id)
            return render(request, "schedules/schedule_confirm_delete.html", {"schedule": schedule})

        schedule = get_object_or_404(Schedule, id=schedule_id) if schedule_id else None
        form = ScheduleForm(instance=schedule)
        return render(request, "schedules/schedule_form.html", {"form": form, "schedule": schedule})

    def post(self, request, schedule_id=None, action=None):
        """Handles creating, updating, and deleting the schedule"""
        if action == "delete":
            schedule = get_object_or_404(Schedule, id=schedule_id)
            schedule.delete()
            return redirect("schedules:schedule_list")

        schedule = get_object_or_404(Schedule, id=schedule_id) if schedule_id else None
        form = ScheduleForm(request.POST, instance=schedule)

        if form.is_valid():
            schedule = form.save(commit=False)

            # Assign the current user to the schedule
            schedule.user = request.user

            # Geocode locations
            start_coords = geocode_address(schedule.start_location)
            dest_coords = geocode_address(schedule.destination)

            # Handle missing geocoding gracefully
            if start_coords[0]:
                schedule.start_lat, schedule.start_lon = start_coords
            else:
                request.session["geocode_error"] = f"Geocoding failed for start location: {schedule.start_location}"
                schedule = None
                return render(request, "schedules/schedule_form.html", {"form": form, "schedule": schedule})
            if dest_coords[0]:
                schedule.dest_lat, schedule.dest_lon = dest_coords
            else:
                request.session["geocode_error"] = f"Geocoding failed for destination: {schedule.destination}"
                schedule = None
                return render(request, "schedules/schedule_form.html", {"form": form, "schedule": schedule})

            schedule.save()
            # fix below

            return redirect("schedules:schedule_list")

        return render(request, "schedules/schedule_form.html", {"form": form, "schedule": schedule})



def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points."""
    R = 6371  # Earth's radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@login_required
def similar_schedules(request, schedule_id):
    """Find and display schedules similar to the given one."""
    user_schedule = get_object_or_404(Schedule, id=schedule_id)

    # Get time before and after arrival
    before = mins_before(user_schedule, -30)
    after = mins_before(user_schedule, 30)

    # Get schedules with similar day and arrival times
    possible_schedules = Schedule.objects.filter(
        day_available=user_schedule.day_available,
        arrival_time__gte=before,
        arrival_time__lte=after,
    ).exclude(user=user_schedule.user)

    # Calculate distances for filtering and displaying
    matching_schedules = []
    for schedule in possible_schedules:
        start_distance = haversine(user_schedule.start_lat, user_schedule.start_lon,
                                   schedule.start_lat, schedule.start_lon)
        dest_distance = haversine(user_schedule.dest_lat, user_schedule.dest_lon,
                                  schedule.dest_lat, schedule.dest_lon)

        if dest_distance <= 5:  # Only include schedules within 5km of destination
            matching_schedules.append({
                "user": schedule.user,
                "arrival_time": schedule.arrival_time,
                "start_distance": round(start_distance, 2),  # Rounded for readability
                "dest_distance": round(dest_distance, 2),
            })

    return render(request, "schedules/similar_schedules.html", {
        "schedule": user_schedule,
        "matches": matching_schedules,
    })



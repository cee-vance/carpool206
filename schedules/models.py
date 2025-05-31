
from django.db import models
import requests
# Create your models here.

from django.conf import settings

DAYS = [(1,"Mondays"),
        (2,"Tuesdays"),
        (3,"Wednesdays"),
        (4,"Thursdays"),
        (5,"Fridays"),
        (6,"Saturdays"),
        (7,"Sundays")]


class Schedule(models.Model):
    """Stores user schedules with geocodable locations."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_location = models.CharField(max_length=255)  # User-input address
    destination = models.CharField(max_length=255)  # User-input address
    start_lat = models.FloatField(null=True, blank=True)
    start_lon = models.FloatField(null=True, blank=True)
    dest_lat = models.FloatField(null=True, blank=True)
    dest_lon = models.FloatField(null=True, blank=True)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    day_available = models.IntegerField(max_length=1,choices=DAYS)#models.JSONField(default=list)  # Example: ["Monday", "Wednesday", "Friday"]

    def __str__(self):
        return f"{self.user.username} | {self.start_location} -> {self.destination}"







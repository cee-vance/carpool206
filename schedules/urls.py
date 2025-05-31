from django.urls import path
from .views import ScheduleView, schedule_list, similar_schedules

app_name = 'schedules'

urlpatterns = [
    path("", ScheduleView.as_view(), name="schedule_create"),
    path("<int:schedule_id>/", ScheduleView.as_view(), name="schedule_edit"),
    path("<int:schedule_id>/<str:action>/", ScheduleView.as_view(), name="schedule_delete"),
    path("list/", schedule_list, name="schedule_list"),
    path('schedules/<int:schedule_id>/matches/', similar_schedules, name='similar_schedules'),
]

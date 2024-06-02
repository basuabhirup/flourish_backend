
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("events", views.all_events, name="all_events"),
    path("events/<int:event_id>", views.event_detail, name="event_detail")
]
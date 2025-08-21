# server/routing.py
from django.urls import re_path
from track.consumer import RiderTrackerConsumer

websocket_urlpatterns = [
    re_path(r"ws/riders/$", RiderTrackerConsumer.as_asgi()),
]

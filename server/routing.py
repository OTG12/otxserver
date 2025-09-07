from django.urls import re_path
from track.consumer import RiderTrackerConsumer

websocket_urlpatterns = [
    # all riders
    re_path(r"ws/riders/?$", RiderTrackerConsumer.as_asgi()),

    # specific rider by id
    re_path(r"ws/riders/(?P<rider_id>[0-9A-Fa-f\-]+)/?$", RiderTrackerConsumer.as_asgi()),


]

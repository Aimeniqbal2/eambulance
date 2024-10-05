from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/emergency/(?P<user_id>\d+)/$', consumers.EmergencyRequestConsumer.as_asgi()),
    # re_path(r'ws/ambulance/(?P<request_id>\d+)/$', consumers.AmbulanceConsumer.as_asgi()),
    # re_path(r'ws/driver/requests/$', consumers.DriverRequestsConsumer.as_asgi()),
]

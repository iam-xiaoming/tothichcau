from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<stream_id>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
]
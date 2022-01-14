from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/<str:roomname>/', consumers.ChatConsumer.as_asgi()),
]
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "rooms"

urlpatterns = [
    path("salas/", views.room, name="room"),
    path("salas/remover/", views.room_delete, name="room_delete"),
    path("salas/remover/participante/", views.room_remove_participant, name="room_remove_participant"),
]

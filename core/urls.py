from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("perfil/", views.profile, name="profile"),
]

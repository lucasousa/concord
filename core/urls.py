from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("perfil/", views.profile, name="profile"),
    path('entrar/', auth_views.LoginView.as_view(
        template_name='core/login.html',
        redirect_authenticated_user=True
    ),  name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
]

from concord import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path(
        "entrar/",
        auth_views.LoginView.as_view(
            template_name="core/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("chat/<uuid:uuid>/", views.chat, name="chat"),
    path("users/<int:room>/", views.users_without_rooms, name="users_without_rooms"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

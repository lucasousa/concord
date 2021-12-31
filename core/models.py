from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from django.db import models
import uuid


class BaseModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    STATUS_ONLINE = "online"
    STATUS_OFFLINE = "online"

    STATUS_CHOICE = (
        (STATUS_ONLINE, "online"),
        (STATUS_OFFLINE, "offline")
    )
    name = models.CharField("Nome", max_length=50, null=False, blank=False)
    username = models.CharField("Username", max_length=50, unique=True)
    image = models.ImageField("Imagem", upload_to="media/avatar", null=True, blank=True)
    last_ping = models.DateField("Visto por último", null=True, blank=True)
    status = models.CharField("Status", choices=STATUS_CHOICE, max_length=10, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        ordering = ["name"]
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
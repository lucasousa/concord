from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid
from django.core import validators
import re


from core.managers import UserManager


class BaseModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    STATUS_ONLINE = "online"
    STATUS_OFFLINE = "offline"

    STATUS_CHOICES = ((STATUS_ONLINE, "online"), (STATUS_OFFLINE, "offline"))
    name = models.CharField("Nome", max_length=50, null=False, blank=False)
    username = models.CharField("Username", max_length=50, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome de usuário válido. '
                'Este valor deve conter apenas letras, números '
                'e os caracteres: @/./+/-/_ .'
                , 'invalid'
            )
        ],)
    image = models.ImageField("Imagem", upload_to="media/avatar", default="default.jpg", null=True, blank=True)
    last_ping = models.DateTimeField("Visto por último", null=True, blank=True)
    status = models.CharField(
        "Status", choices=STATUS_CHOICES, max_length=10, default=STATUS_OFFLINE, blank=True, null=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ["name"]
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

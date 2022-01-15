from core.models import BaseModel
from django.db import models


class Room(BaseModel):
    name = models.CharField("Nome da sala", max_length=50)
    every_one_send_message = models.BooleanField(
        "Todos podem enviar mensagem ?", default=True
    )
    type = models.CharField("Tipo", max_length=10)
    user = models.ManyToManyField("core.User", verbose_name="Usuário", blank=False)

    @property
    def one_a_one(self):
        return self.user.count() == 2 and self.every_one_send_message

    def __str__(self) -> str:
        return self.name

    @property
    def get_users(self):
        response = []
        for user in self.user.all():
            response.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "room": self.id,
                }
            )

        return response

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sala"
        verbose_name_plural = "Salas"


class Message(BaseModel):
    user = models.ForeignKey(
        "core.User",
        verbose_name="Usuário",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    room = models.ForeignKey("Room", verbose_name="Sala", on_delete=models.CASCADE)
    text = models.TextField("Texto da mensagem", null=True, blank=True)
    file = models.FileField(
        "Arquivo", upload_to="media/file", max_length=254, null=True, blank=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": str(self.created_at),
            "update_at": str(self.updated_at),
            "user": self.user.name,
            "room": str(self.room.uuid),
            "text": self.text,
            "file": self.file.url if self.file else None,
        }

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

from django.db import models

from core.models import BaseModel


class Room(BaseModel):
    name = models.CharField("Nome da sala", max_length=50)
    every_one_send_message = models.BooleanField(
        "Todos podem enviar mensagem ?", default=True
    )
    type = models.CharField("Tipo", max_length=10)
    user = models.ManyToManyField("core.User", verbose_name="Usuário", blank=False)

    def __str__(self) -> str:
        return self.name

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

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

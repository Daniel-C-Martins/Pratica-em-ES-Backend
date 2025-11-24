from django.db import models
from django.conf import settings

from api.models.ong import Ong


class Tutor(models.Model):
    id_tutor = models.AutoField(db_column="id_tutor", primary_key=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tutor",
        db_column="id_user",
        null=True,
        blank=True,
    )

    nome = models.CharField(db_column="nome", max_length=100, blank=False, null=False)

    cpf = models.CharField(
        db_column="cpf", max_length=11, blank=False, null=False, unique=True
    )

    telefone = models.CharField(
        db_column="telefone", max_length=15, blank=False, null=False, unique=True
    )

    ong = models.ForeignKey(
        to=Ong,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        db_column="id_ong",
    )

    class Meta:
        db_table = "tutor"

    def __str__(self):
        return f"{self.nome} - {self.user.email} - {self.telefone} - {self.ong}"

    def __repr__(self):
        return (
            f"Tutor(id_tutor={self.id_tutor}, nome={self.nome}, "
            f"email={self.user.email}, telefone={self.telefone}, ong={self.ong})"
        )

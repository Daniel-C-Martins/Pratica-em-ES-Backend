from django.db import models

from api.models.pet import Pet


class Rastreio(models.Model):

    id_rastreio = models.AutoField(db_column="id_rastreio", primary_key=True)

    estado_rastreio = models.CharField(
        db_column="estado_rastreio", max_length=100, blank=False, null=False
    )

    descricao_rastreio = models.TextField(
        db_column="descricao_rastreio", blank=True, null=True
    )

    data_atualizacao = models.DateTimeField(
        db_column="data_atualizacao", auto_now=True, blank=False, null=False
    )

    pet = models.ForeignKey(
        to=Pet, blank=False, null=False, on_delete=models.CASCADE, db_column="id_pet"
    )

    class Meta:
        db_table = "rastreio"

    def __str__(self):
        return f"{self.estado_rastreio}"

    def __repr__(self):
        return f"Rastreio(id_rastreio={self.id_rastreio}, estado_rastreio={self.estado_rastreio})"

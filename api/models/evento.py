from django.db import models

from api.models.adocao import Adocao


class Evento(models.Model):
    id_evento = models.AutoField(db_column="id_evento", primary_key=True)

    data = models.DateField(db_column="data", blank=False, null=False)

    descricao = models.TextField(db_column="descricao", blank=True, null=True)

    adocao = models.ForeignKey(
        to=Adocao, blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta:
        db_table = "evento"

    def __str__(self):
        return f"Evento {self.id_evento} - {self.data}"

    def __repr__(self):
        return f"Evento(id_evento={self.id_evento}, data={self.data})"

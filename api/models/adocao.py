from django.db import models

from api.models.pet import Pet
from api.models.adotante import Adotante


class StatusAdocao(models.IntegerChoices):
    EM_ANDAMENTO = 1, "Em Andamento"
    REJEITADA = 2, "Rejeitada"
    CONCLUIDA = 3, "Concluída"


class Adocao(models.Model):
    id = models.AutoField(db_column="id_adocao", primary_key=True)

    data_adocao = models.DateField(db_column="data_adocao", blank=False)

    status = models.IntegerField(
        db_column="status", choices=StatusAdocao.choices, blank=False, null=False
    )

    pet = models.ForeignKey(to=Pet, blank=False, null=False, on_delete=models.CASCADE)

    adotante = models.ForeignKey(
        to=Adotante, blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta:
        db_table = "adocao"

    def __str__(self):
        return f"Adocao(id={self.id}, data_adocao={self.data_adocao}, status={self.status}, pet={self.pet}, adotante={self.adotante})"

    def __repr__(self):
        return f"Adocao(id={self.id}, data_adocao={self.data_adocao}, status={self.status}, pet={self.pet}, adotante={self.adotante})"

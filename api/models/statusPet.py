from django.db import models


class Status(models.IntegerChoices):
    DISPONIVEL = 1, "Disponível"
    PERDIDO = 2, "Perdido"
    FALECIDO = 3, "Falecido"
    ADOTADO = 4, "Adotado"


class StatusPet(models.Model):
    id_status_pet = models.AutoField(db_column="id_status_pet", primary_key=True)

    status = models.IntegerField(
        db_column="status", choices=Status.choices, blank=False, null=False
    )

    class Meta:
        db_table = "status_pet"

    def __str__(self):
        return f"{self.status}"

    def __repr__(self):
        return f"StatusPet(id_status_pet={self.id_status_pet}, status={self.status})"

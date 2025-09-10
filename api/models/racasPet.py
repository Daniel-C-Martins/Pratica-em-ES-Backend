from django.db import models

from api.models.especiePet import EspeciePet


class RacasPet(models.Model):
    id_raca_pet = models.AutoField(db_column="id_raca_pet", primary_key=True)

    raca = models.CharField(db_column="raca", max_length=100, blank=False, null=False)

    especie = models.ForeignKey(
        to=EspeciePet, blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta:
        db_table = "racas_pet"

    def __str__(self):
        return f"{self.raca}"

    def __repr__(self):
        return f"RacasPet(id_raca_pet={self.id_raca_pet}, raca={self.raca})"

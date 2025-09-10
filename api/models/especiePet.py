from django.db import models


class EspeciePet(models.Model):
    id_especie_pet = models.AutoField(db_column="id_especie_pet", primary_key=True)

    especie = models.CharField(
        db_column="especie", max_length=100, blank=False, null=False
    )

    class Meta:
        db_table = "especie_pet"

    def __str__(self):
        return f"{self.especie}"

    def __repr__(self):
        return (
            f"EspeciePet(id_especie_pet={self.id_especie_pet}, especie={self.especie})"
        )

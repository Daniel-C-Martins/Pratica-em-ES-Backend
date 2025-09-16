from django.db import models

from api.models.especiePet import EspeciePet
from api.models.racasPet import RacasPet


class Adotante(models.Model):
    id = models.AutoField(db_column="id_adotante", primary_key=True)

    nome = models.CharField(db_column="nome", max_length=100, blank=False)

    email = models.EmailField(db_column="email", max_length=100, blank=False)

    telefone = models.CharField(db_column="telefone", max_length=15, blank=False)

    

    class Meta:
        db_table = "adotante"

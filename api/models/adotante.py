from django.db import models

from api.models.especiePet import EspeciePet
from api.models.racasPet import RacasPet


class Adotante(models.Model):
    id = models.AutoField(db_column="id_adotante", primary_key=True)

    nome = models.CharField(db_column="nome", max_length=100, blank=False)

    email = models.EmailField(db_column="email", max_length=100, blank=False)

    telefone = models.CharField(db_column="telefone", max_length=15, blank=False)

    preferencia_porte = models.CharField(
        db_column="preferencia_porte", max_length=50, blank=True, null=True
    )

    preferencia_idade = models.CharField(
        db_column="preferencia_idade", max_length=50, blank=True, null=True
    )

    preferencia_sexo = models.CharField(
        db_column="preferencia_sexo", max_length=10, blank=True, null=True
    )

    aceita_doenca_cronica = models.BooleanField(
        db_column="aceita_doenca_cronica", blank=False, default=False
    )

    aceita_necessidades_especiais = models.BooleanField(
        db_column="aceita_necessidades_especiais", blank=False, default=False
    )

    possui_outros_animais = models.BooleanField(
        db_column="possui_outros_animais", blank=False, default=False
    )

    possui_tempo = models.BooleanField(
        db_column="possui_tempo", blank=False, default=False
    )

    preferencia_especie = models.ForeignKey(
        to=EspeciePet,
        db_column="preferencia_especie",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )

    preferencia_raca = models.ForeignKey(
        to=RacasPet,
        db_column="preferencia_raca",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = "adotante"

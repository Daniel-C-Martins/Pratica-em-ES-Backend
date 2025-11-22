from django.db import models
from api.models.especiePet import EspeciePet
from api.models.racasPet import RacasPet
from api.models.adotante import Adotante


class IdadePet(models.IntegerChoices):
    FILHOTE = 1, "Filhote"
    ADULTO = 2, "Adulto"
    IDOSO = 3, "Idoso"
    INDIFERENTE = 4, "Indiferente"


class PortePet(models.IntegerChoices):
    PEQUENO = 1, "Pequeno"
    MEDIO = 2, "Médio"
    GRANDE = 3, "Grande"
    MUITO_GRANDE = 4, "Muito Grande"
    INDIFERENTE = 5, "Indiferente"


class SexoPet(models.IntegerChoices):
    M = 1, "Macho"
    F = 2, "Fêmea"
    INDIFERENTE = 3, "Indiferente"


class PreferenciaAdotante(models.Model):
    preferencia_porte = models.IntegerField(
        db_column="preferencia_porte", choices=PortePet.choices, blank=True, null=True
    )

    preferencia_idade = models.IntegerField(
        db_column="preferencia_idade", choices=IdadePet.choices, blank=True, null=True
    )

    preferencia_sexo = models.IntegerField(
        db_column="preferencia_sexo", choices=SexoPet.choices, blank=True, null=True
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

    adotante = models.ForeignKey(
        to=Adotante,
        db_column="adotante",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )

    preferencia_ativa = models.BooleanField(
        db_column="preferencia_ativa", blank=False, default=True
    )

    def __str__(self):
        return f"{self.adotante} - {self.preferencia_especie} - {self.preferencia_raca} - {self.data_registro}"

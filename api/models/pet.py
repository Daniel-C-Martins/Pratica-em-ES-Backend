from django.db import models
from django.db.models import Q

from api.models.especiePet import EspeciePet
from api.models.statusPet import StatusPet
from api.models.ong import Ong
from api.models.tutor import Tutor


class IdadePet(models.IntegerChoices):
    FILHOTE = 1, "Filhote"
    ADULTO = 2, "Adulto"
    IDOSO = 3, "Idoso"


class Pet(models.Model):
    id_pet = models.AutoField(db_column="id_pet", primary_key=True)

    nome = models.CharField(db_column="nome", max_length=100, blank=False, null=False)

    idade = models.IntegerField(
        db_column="idade", blank=False, null=False, choices=IdadePet.choices
    )

    porte = models.CharField(db_column="porte", max_length=50, blank=False, null=False)

    descricao = models.TextField(db_column="descricao", blank=True, null=True)

    foto = models.TextField(db_column="foto", blank=True, null=True)

    doenca_cronica = models.BooleanField(
        db_column="doenca_cronica", blank=False, null=False, default=False
    )

    necessidades_especiais = models.BooleanField(
        db_column="necessidades_especiais", blank=False, null=False, default=False
    )

    cuidados_constantes = models.BooleanField(
        db_column="cuidados_constantes", blank=False, null=False, default=False
    )

    amigavel_outros_animais = models.BooleanField(
        db_column="amigavel_outros_animais", blank=False, null=False, default=False
    )

    especie = models.ForeignKey(
        to=EspeciePet, blank=False, null=False, on_delete=models.PROTECT
    )

    status_pet = models.ForeignKey(
        to=StatusPet, blank=False, null=False, on_delete=models.PROTECT
    )

    ong = models.ForeignKey(to=Ong, blank=True, null=True, on_delete=models.PROTECT)

    tutor = models.ForeignKey(to=Tutor, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        db_table = "pet"
        constraints = [
            models.CheckConstraint(
                name="pet_owner_xor",
                check=(
                    (Q(ong__isnull=False) & Q(tutor__isnull=True))
                    | (Q(ong__isnull=True) & Q(tutor__isnull=False))
                ),
            )
        ]

    @property
    def owner(self):
        return self.tutor or self.ong

    @property
    def owner_type(self):
        return "tutor" if self.tutor_id else "ong"

    def __str__(self):
        return f"{self.nome} - {self.idade} anos - {self.porte} - {self.foto}"

    def __repr__(self):
        return f"Pet(id_pet={self.id_pet}, nome={self.nome}, idade={self.idade}, porte={self.porte}, descricao={self.descricao}, foto={self.foto})"

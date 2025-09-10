from django.db import models


class Ong(models.Model):
    id_ong = models.AutoField(db_column="id_ong", primary_key=True)

    nome = models.CharField(db_column="nome", max_length=100, blank=False, null=False)

    email = models.EmailField(
        db_column="email", max_length=100, blank=False, null=False, unique=True
    )

    cnpj = models.CharField(db_column="cnpj", max_length=15, blank=False, null=False)

    telefone = models.CharField(
        db_column="telefone", max_length=15, blank=False, null=False, unique=True
    )

    endereco = models.CharField(
        db_column="endereco", max_length=255, blank=False, null=False
    )

    cidade = models.CharField(
        db_column="cidade", max_length=100, blank=False, null=False
    )

    estado = models.CharField(
        db_column="estado", max_length=100, blank=False, null=False
    )

    class Meta:
        db_table = "ong"

    def __str__(self):
        return f"{self.nome} - {self.email}"

    def __repr__(self):
        return f"Ong(id_ong={self.id_ong}, nome={self.nome}, email={self.email})"

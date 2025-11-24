from django.db import models
from django.conf import settings  

class Adotante(models.Model):
    id = models.AutoField(db_column="id_adotante", primary_key=True)


    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="adotante",
        db_column="id_user",
        null=True,
        blank=True,
    )

    nome = models.CharField(db_column="nome", max_length=100, blank=False)

    telefone = models.CharField(db_column="telefone", max_length=15, blank=False)

    class Meta:
        db_table = "adotante"

    def __str__(self):
        return f"{self.nome} ({self.user.email})"

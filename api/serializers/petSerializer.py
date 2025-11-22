from rest_framework import serializers
from api.models.pet import Pet


class PetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"


class PetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"


class PetScoreSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(read_only=True)

    class Meta:
        model = Pet
        fields = [
            "id_pet",
            "nome",
            "idade",
            "porte",
            "descricao",
            "foto",
            "sexo",
            "doenca_cronica",
            "necessidades_especiais",
            "cuidados_constantes",
            "amigavel_outros_animais",
            "especie",
            "status_pet",
            "ong",
            "tutor",
            "raca",
            "score",
        ]

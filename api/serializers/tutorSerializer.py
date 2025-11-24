from rest_framework import serializers
from api.models.tutor import Tutor


class TutorReadSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Tutor
        fields = (
            "id_tutor",
            "nome",
            "cpf",
            "telefone",
            "ong",
            "email",
        )


class TutorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = (
            "id_tutor",
            "user",
            "nome",
            "cpf",
            "telefone",
            "ong",
        )
        read_only_fields = ("id_tutor",)

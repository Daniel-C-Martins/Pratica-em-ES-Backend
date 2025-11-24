from rest_framework import serializers
from api.models.adotante import Adotante


class AdotanteReadSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Adotante
        fields = ("id", "nome", "telefone", "email")


class AdotanteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adotante
        fields = ("nome", "telefone")
        extra_kwargs = {
            "nome": {"required": True},
            "telefone": {"required": True},
        }

    def create(self, validated_data):
        user = self.context.get("user")
        if user is None:
            raise ValueError("User não fornecido no contexto do serializer.")
        return Adotante.objects.create(user=user, **validated_data)

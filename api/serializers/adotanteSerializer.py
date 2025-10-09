from rest_framework import serializers

from api.models.adotante import Adotante


class AdotanteReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adotante
        fields = "__all__"


class AdotanteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adotante
        fields = "__all__"

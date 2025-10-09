from rest_framework import serializers

from api.models.preferenciaAdotante import PreferenciaAdotante


class PreferenciaAdotanteReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenciaAdotante
        fields = "__all__"


class PreferenciaAdotanteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenciaAdotante
        fields = "__all__"

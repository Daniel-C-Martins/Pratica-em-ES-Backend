from rest_framework import serializers
from api.models.rastreio import Rastreio


class RastreioReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rastreio
        fields = "__all__"


class RastreioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rastreio
        fields = "__all__"

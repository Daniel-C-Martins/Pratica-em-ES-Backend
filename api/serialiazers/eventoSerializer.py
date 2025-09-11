from rest_framework import serializers
from api.models.evento import Evento


class EventoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = "__all__"


class EventoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = "__all__"

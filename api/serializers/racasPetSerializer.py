from rest_framework import serializers
from api.models.racasPet import RacasPet


class RacasPetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RacasPet
        fields = "__all__"


class RacasPetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RacasPet
        fields = "__all__"

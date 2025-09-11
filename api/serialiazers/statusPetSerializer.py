from rest_framework import serializers
from api.models.statusPet import StatusPet


class StatusPetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusPet
        fields = "__all__"


class StatusPetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusPet
        fields = "__all__"

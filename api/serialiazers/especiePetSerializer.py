from rest_framework import serializers
from api.models.especiePet import EspeciePet


class EspeciePetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EspeciePet
        fields = "__all__"


class EspeciePetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EspeciePet
        fields = "__all__"

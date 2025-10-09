from rest_framework import serializers
from api.models.ong import Ong


class OngReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ong
        fields = "__all__"


class OngWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ong
        fields = "__all__"

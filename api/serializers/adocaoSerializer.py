from rest_framework import serializers
from api.models.adocao import Adocao


class AdocaoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adocao
        fields = "__all__"


class AdocaoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adocao
        fields = "__all__"

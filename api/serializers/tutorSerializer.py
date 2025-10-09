from rest_framework import serializers
from api.models.tutor import Tutor


class TutorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = "__all__"


class TutorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = "__all__"

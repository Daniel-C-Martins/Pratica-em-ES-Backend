# api/serializers/authSerializer.py
from rest_framework import serializers

from api.models.user import User
from api.models.adotante import Adotante
from api.models.tutor import Tutor
from api.models.ong import Ong


class RegisterAdotanteSerializer(serializers.Serializer):
    # dados de login
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    # dados do perfil Adotante
    nome = serializers.CharField(max_length=100)
    telefone = serializers.CharField(max_length=15)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Já existe um usuário com esse e-mail.")
        return value

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            email=email,
            password=password,
            role=User.Role.ADOTANTE,
        )

        adotante = Adotante.objects.create(
            user=user,
            **validated_data,
        )

        return adotante


class RegisterTutorSerializer(serializers.Serializer):
    # dados de login
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    # dados do perfil Tutor
    nome = serializers.CharField(max_length=100)
    cpf = serializers.CharField(max_length=11)
    telefone = serializers.CharField(max_length=15)
    ong_id = serializers.IntegerField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Já existe um usuário com esse e-mail.")
        return value

    def validate_ong_id(self, value):
        if not Ong.objects.filter(pk=value).exists():
            raise serializers.ValidationError("ONG não encontrada.")
        return value

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        ong_id = validated_data.pop("ong_id")

        user = User.objects.create_user(
            email=email,
            password=password,
            role=User.Role.TUTOR,
        )

        ong = Ong.objects.get(pk=ong_id)

        tutor = Tutor.objects.create(
            user=user,
            ong=ong,
            **validated_data,  # nome, cpf, telefone
        )

        return tutor

# api/views/adotanteView.py (por exemplo)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.adotante import Adotante
from api.models.user import User
from api.serializers.adotanteSerializer import (
    AdotanteReadSerializer,
    AdotanteWriteSerializer,
)
from api.serializers.authSerializer import RegisterAdotanteSerializer


class AdotanteView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Lista todos os adotantes.",
        responses={200: AdotanteReadSerializer(many=True)},
    )
    def get(self, request):
        adotantes = Adotante.objects.all()
        serializer = AdotanteReadSerializer(adotantes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Cria um adotante para o usuário autenticado.",
        request=AdotanteWriteSerializer,
        responses={
            201: AdotanteReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Autenticação necessária."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = AdotanteWriteSerializer(
            data=request.data,
            context={"user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        adotante = serializer.save()
        read_serializer = AdotanteReadSerializer(adotante)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class AdotanteDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Busca um adotante pelo ID.",
        responses={
            200: AdotanteReadSerializer,
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def get(self, request, pk):
        adotante = get_object_or_404(Adotante, pk=pk)
        serializer = AdotanteReadSerializer(adotante)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Atualiza completamente um adotante.",
        request=AdotanteWriteSerializer,
        responses={
            200: AdotanteReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def put(self, request, pk):
        adotante = get_object_or_404(Adotante, pk=pk)
        serializer = AdotanteWriteSerializer(
            adotante,
            data=request.data,
            context={"user": adotante.user},
        )
        serializer.is_valid(raise_exception=True)
        adotante = serializer.save()
        read_serializer = AdotanteReadSerializer(adotante)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Exclui um adotante.",
        responses={
            204: OpenApiResponse(description="Deletado com sucesso"),
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def delete(self, request, pk):
        adotante = get_object_or_404(Adotante, pk=pk)
        adotante.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdotantePorUsuarioView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Busca um adotante pelo ID do usuário.",
        responses={
            200: AdotanteReadSerializer,
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def get(self, request, user_id):
        try:
            adotante = get_object_or_404(Adotante, user_id=user_id)
            serializer = AdotanteReadSerializer(adotante)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAdotanteView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Registra um novo usuário adotante (User + Adotante) e retorna tokens JWT.",
        request=RegisterAdotanteSerializer,
        responses={
            201: OpenApiResponse(
                description="Usuário adotante criado com sucesso (user, perfil e tokens)."
            ),
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        serializer = RegisterAdotanteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        adotante = serializer.save()
        user: User = adotante.user

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
                "adotante": AdotanteReadSerializer(adotante).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )

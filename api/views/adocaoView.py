# views/adocao.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.adocao import Adocao
from api.serializers.adocaoSerializer import (
    AdocaoReadSerializer,
    AdocaoWriteSerializer,
)


class AdocaoView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        description="Lista todas as adoções.",
        responses={200: AdocaoReadSerializer(many=True)},
    )
    def get(self, request):
        try:
            adocoes = Adocao.objects.all()
            serializer = AdocaoReadSerializer(adocoes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Cria uma adoção.",
        # Aqui você define O QUE O BODY DEVE TER:
        request=AdocaoWriteSerializer,
        responses={
            201: AdocaoReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        try:
            serializer = AdocaoWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdocaoDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Busca uma adoção pelo ID.",
        responses={200: AdocaoReadSerializer, 404: OpenApiResponse(description="Não encontrado")},
    )
    def get(self, request, pk):
        try:
            adocao = get_object_or_404(Adocao, pk=pk)
            serializer = AdocaoReadSerializer(adocao)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza completamente uma adoção.",
        request=AdocaoWriteSerializer,
        responses={200: AdocaoReadSerializer, 400: OpenApiResponse(description="Erro de validação")},
    )
    def put(self, request, pk):
        try:
            adocao = get_object_or_404(Adocao, pk=pk)
            serializer = AdocaoWriteSerializer(adocao, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Exclui uma adoção.",
        responses={204: OpenApiResponse(description="Deletado com sucesso"),
                   404: OpenApiResponse(description="Não encontrado")},
    )
    def delete(self, request, pk):
        try:
            adocao = get_object_or_404(Adocao, pk=pk)
            adocao.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdocaoPorUsuarioView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Busca todas as adoções de um usuário pelo ID do usuário.",
        responses={
            200: AdocaoReadSerializer(many=True),
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def get(self, request, user_id):
        try:
            adocoes = Adocao.objects.filter(adotante__user_id=user_id)
            serializer = AdocaoReadSerializer(adocoes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PetAdotadoView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Verifica se um pet foi adotado (status concluída).",
        responses={
            200: OpenApiResponse(description="Retorna se o pet foi adotado"),
            400: OpenApiResponse(description="Erro na requisição"),
        },
    )
    def get(self, request, pet_id):
        try:
            from api.models.adocao import StatusAdocao

            adotado = Adocao.objects.filter(
                pet_id=pet_id,
                status=StatusAdocao.CONCLUIDA
            ).exists()

            return Response({"adotado": adotado}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

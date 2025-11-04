from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.adotante import Adotante
from api.serializers.adotanteSerializer import (
    AdotanteReadSerializer,
    AdotanteWriteSerializer,
)


class AdotanteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Lista todos os adotantes.",
        responses={200: AdotanteReadSerializer(many=True)},
    )
    def get(self, request):
        try:
            adotantes = Adotante.objects.all()
            serializer = AdotanteReadSerializer(adotantes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Cria um adotante.",
        request=AdotanteWriteSerializer,   
        responses={
            201: AdotanteReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        try:
            serializer = AdotanteWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdotanteDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Busca um adotante pelo ID.",
        responses={200: AdotanteReadSerializer, 404: OpenApiResponse(description="Não encontrado")},
    )
    def get(self, request, pk):
        try:
            adotante = get_object_or_404(Adotante, pk=pk)
            serializer = AdotanteReadSerializer(adotante)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza completamente um adotante.",
        request=AdotanteWriteSerializer,   # <- Body do PUT
        responses={200: AdotanteReadSerializer, 400: OpenApiResponse(description="Erro de validação")},
    )
    def put(self, request, pk):
        try:
            adotante = get_object_or_404(Adotante, pk=pk)
            serializer = AdotanteWriteSerializer(adotante, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Exclui um adotante.",
        responses={204: OpenApiResponse(description="Deletado com sucesso"),
                   404: OpenApiResponse(description="Não encontrado")},
    )
    def delete(self, request, pk):
        try:
            adotante = get_object_or_404(Adotante, pk=pk)
            adotante.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

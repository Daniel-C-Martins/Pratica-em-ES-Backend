from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.preferenciaAdotante import PreferenciaAdotante
from api.serializers.preferenciaAdotanteSerializer import (
    PreferenciaAdotanteReadSerializer,
    PreferenciaAdotanteWriteSerializer,
)


class PreferenciaAdotanteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Lista todas as preferências de adotantes.",
        responses={200: PreferenciaAdotanteReadSerializer(many=True)},
    )
    def get(self, request):
        try:
            preferencias = PreferenciaAdotante.objects.all()
            serializer = PreferenciaAdotanteReadSerializer(preferencias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Cria uma preferência de adotante.",
        request=PreferenciaAdotanteWriteSerializer,  
        responses={
            201: PreferenciaAdotanteReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        try:
            serializer = PreferenciaAdotanteWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PreferenciaAdotanteDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Busca uma preferência de adotante pelo ID.",
        responses={200: PreferenciaAdotanteReadSerializer, 404: OpenApiResponse(description="Não encontrado")},
    )
    def get(self, request, pk):
        try:
            preferencia = get_object_or_404(PreferenciaAdotante, pk=pk)
            serializer = PreferenciaAdotanteReadSerializer(preferencia)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza completamente uma preferência de adotante.",
        request=PreferenciaAdotanteWriteSerializer,  
        responses={200: PreferenciaAdotanteReadSerializer, 400: OpenApiResponse(description="Erro de validação")},
    )
    def put(self, request, pk):
        try:
            preferencia = get_object_or_404(PreferenciaAdotante, pk=pk)
            serializer = PreferenciaAdotanteWriteSerializer(preferencia, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Exclui uma preferência de adotante.",
        responses={
            204: OpenApiResponse(description="Deletado com sucesso"),
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def delete(self, request, pk):
        try:
            preferencia = get_object_or_404(PreferenciaAdotante, pk=pk)
            preferencia.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

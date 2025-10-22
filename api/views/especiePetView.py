from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.especiePet import EspeciePet
from api.serializers.especiePetSerializer import (
    EspeciePetReadSerializer,
    EspeciePetWriteSerializer,
)


class EspeciePetView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Lista todas as espécies de pet.",
        responses={200: EspeciePetReadSerializer(many=True)},
    )
    def get(self, request):
        try:
            especies = EspeciePet.objects.all()
            serializer = EspeciePetReadSerializer(especies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Cria uma espécie de pet.",
        request=EspeciePetWriteSerializer,  
        responses={
            201: EspeciePetReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        try:
            serializer = EspeciePetWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EspeciePetDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Busca uma espécie de pet pelo ID.",
        responses={200: EspeciePetReadSerializer, 404: OpenApiResponse(description="Não encontrado")},
    )
    def get(self, request, pk):
        try:
            especie = get_object_or_404(EspeciePet, pk=pk)
            serializer = EspeciePetReadSerializer(especie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza completamente uma espécie de pet.",
        request=EspeciePetWriteSerializer,  
        responses={200: EspeciePetReadSerializer, 400: OpenApiResponse(description="Erro de validação")},
    )
    def put(self, request, pk):
        try:
            especie = get_object_or_404(EspeciePet, pk=pk)
            serializer = EspeciePetWriteSerializer(especie, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Exclui uma espécie de pet.",
        responses={
            204: OpenApiResponse(description="Deletado com sucesso"),
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def delete(self, request, pk):
        try:
            especie = get_object_or_404(EspeciePet, pk=pk)
            especie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

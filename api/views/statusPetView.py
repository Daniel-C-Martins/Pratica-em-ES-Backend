from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.statusPet import StatusPet
from api.serializers.statusPetSerializer import (
    StatusPetReadSerializer,
    StatusPetWriteSerializer,
)


class StatusPetView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Lista todos os status de pet.",
        responses={200: StatusPetReadSerializer(many=True)},
    )
    def get(self, request):
        try:
            status_pets = StatusPet.objects.all()
            serializer = StatusPetReadSerializer(status_pets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Cria um status de pet.",
        request=StatusPetWriteSerializer,
        responses={
            201: StatusPetReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        try:
            serializer = StatusPetWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StatusPetDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Busca um status de pet pelo ID.",
        responses={
            200: StatusPetReadSerializer,
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def get(self, request, pk):
        try:
            status_pet = get_object_or_404(StatusPet, pk=pk)
            serializer = StatusPetReadSerializer(status_pet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza completamente um status de pet.",
        request=StatusPetWriteSerializer,
        responses={
            200: StatusPetReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def put(self, request, pk):
        try:
            status_pet = get_object_or_404(StatusPet, pk=pk)
            serializer = StatusPetWriteSerializer(status_pet, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Exclui um status de pet.",
        responses={
            204: OpenApiResponse(description="Deletado com sucesso"),
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def delete(self, request, pk):
        try:
            status_pet = get_object_or_404(StatusPet, pk=pk)
            status_pet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

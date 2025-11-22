from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.rastreio import Rastreio
from api.serializers.rastreioSerializer import (
    RastreioReadSerializer,
    RastreioWriteSerializer,
)


class RastreioView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Lista todos os rastreios.",
        responses={200: RastreioReadSerializer(many=True)},
    )
    def get(self, request):
        try:
            rastreios = Rastreio.objects.all()
            serializer = RastreioReadSerializer(rastreios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Cria um rastreio.",
        request=RastreioWriteSerializer,
        responses={
            201: RastreioReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        try:
            serializer = RastreioWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RastreioDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Busca um rastreio pelo ID.",
        responses={
            200: RastreioReadSerializer,
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def get(self, request, pk):
        try:
            rastreio = get_object_or_404(Rastreio, pk=pk)
            serializer = RastreioReadSerializer(rastreio)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza completamente um evento.",
        request=RastreioWriteSerializer,
        responses={
            200: RastreioReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def put(self, request, pk):
        try:
            rastreio = get_object_or_404(Rastreio, pk=pk)
            serializer = RastreioWriteSerializer(rastreio, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Exclui um rastreio.",
        responses={
            204: OpenApiResponse(description="Deletado com sucesso"),
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def delete(self, request, pk):
        try:
            rastreio = get_object_or_404(Rastreio, pk=pk)
            rastreio.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class RastreioPorPet(APIView):
      permission_classes = [IsAuthenticated, IsAdminUser]
   
      @extend_schema(
         description="Lista todos os rastreios de um pet específico.",
         responses={200: RastreioReadSerializer(many=True)},
      )
      def get(self, request, pet_id):
         try:
               rastreios = Rastreio.objects.filter(pet__id_pet=pet_id)
               serializer = RastreioReadSerializer(rastreios, many=True)
               return Response(serializer.data, status=status.HTTP_200_OK)
         except Exception as e:
               return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

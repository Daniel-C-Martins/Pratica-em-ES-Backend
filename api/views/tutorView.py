from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.tutor import Tutor
from api.serializers.tutorSerializer import (
    TutorReadSerializer,
    TutorWriteSerializer,
)


class TutorView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Lista todos os tutores.",
        responses={200: TutorReadSerializer(many=True)},
    )
    def get(self, request):
        try:
            tutors = Tutor.objects.all()
            serializer = TutorReadSerializer(tutors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Cria um tutor.",
        request=TutorWriteSerializer,  # <- Body do POST
        responses={
            201: TutorReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        try:
            serializer = TutorWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TutorDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Busca um tutor pelo ID.",
        responses={200: TutorReadSerializer, 404: OpenApiResponse(description="Não encontrado")},
    )
    def get(self, request, pk):
        try:
            tutor = get_object_or_404(Tutor, pk=pk)
            serializer = TutorReadSerializer(tutor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza completamente um tutor.",
        request=TutorWriteSerializer,  # <- Body do PUT
        responses={200: TutorReadSerializer, 400: OpenApiResponse(description="Erro de validação")},
    )
    def put(self, request, pk):
        try:
            tutor = get_object_or_404(Tutor, pk=pk)
            serializer = TutorWriteSerializer(tutor, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Exclui um tutor.",
        responses={
            204: OpenApiResponse(description="Deletado com sucesso"),
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def delete(self, request, pk):
        try:
            tutor = get_object_or_404(Tutor, pk=pk)
            tutor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

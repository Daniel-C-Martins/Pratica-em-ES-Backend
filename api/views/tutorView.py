# api/views/tutorView.py (exemplo)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.tutor import Tutor
from api.models.user import User
from api.serializers.authSerializer import RegisterTutorSerializer
from api.serializers.tutorSerializer import (
    TutorReadSerializer,
    TutorWriteSerializer,
)


class TutorView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Lista todos os tutores.",
        responses={200: TutorReadSerializer(many=True)},
    )
    def get(self, request):
        tutors = Tutor.objects.all()
        serializer = TutorReadSerializer(tutors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Cria um tutor (CRUD admin).",
        request=TutorWriteSerializer,
        responses={
            201: TutorReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        serializer = TutorWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tutor = serializer.save()
        return Response(TutorReadSerializer(tutor).data, status=status.HTTP_201_CREATED)


class TutorDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Busca um tutor pelo ID.",
        responses={200: TutorReadSerializer, 404: OpenApiResponse(description="Não encontrado")},
    )
    def get(self, request, pk):
        tutor = get_object_or_404(Tutor, pk=pk)
        serializer = TutorReadSerializer(tutor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Atualiza completamente um tutor.",
        request=TutorWriteSerializer,
        responses={200: TutorReadSerializer, 400: OpenApiResponse(description="Erro de validação")},
    )
    def put(self, request, pk):
        tutor = get_object_or_404(Tutor, pk=pk)
        serializer = TutorWriteSerializer(tutor, data=request.data)
        serializer.is_valid(raise_exception=True)
        tutor = serializer.save()
        return Response(TutorReadSerializer(tutor).data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Exclui um tutor.",
        responses={
            204: OpenApiResponse(description="Deletado com sucesso"),
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def delete(self, request, pk):
        tutor = get_object_or_404(Tutor, pk=pk)
        tutor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TutorPorUsuarioView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Busca um tutor pelo ID do usuário.",
        responses={
            200: TutorReadSerializer,
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def get(self, request, user_id):
        try:
            tutor = get_object_or_404(Tutor, user_id=user_id)
            serializer = TutorReadSerializer(tutor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterTutorView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Registra um novo usuário tutor (User + Tutor) e retorna tokens JWT.",
        request=RegisterTutorSerializer,
        responses={
            201: OpenApiResponse(
                description="Usuário tutor criado com sucesso (user, perfil e tokens)."
            ),
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        serializer = RegisterTutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tutor = serializer.save()
        user: User = tutor.user

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
                "tutor": TutorReadSerializer(tutor).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.models.pet import Pet
from api.serializers.petSerializer import (
    PetReadSerializer,
    PetWriteSerializer,
    PetScoreSerializer,
)


class PetView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Lista todos os pets.",
        responses={200: PetReadSerializer(many=True)},
    )
    def get(self, request):
        try:
            pets = Pet.objects.all()

            especie = request.query_params.get("especie")
            raca = request.query_params.get("raca")
            porte = request.query_params.get("porte")
            sexo = request.query_params.get("sexo")

            if especie:
                pets = pets.filter(especie=especie)

            if raca:
                pets = pets.filter(raca=raca)

            if porte:
                pets = pets.filter(porte=porte)

            if sexo:
                pets = pets.filter(sexo=sexo)

            serializer = PetReadSerializer(pets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Cria um pet.",
        request=PetWriteSerializer,
        responses={
            201: PetReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def post(self, request):
        try:
            serializer = PetWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PetDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Busca um pet pelo ID.",
        responses={
            200: PetReadSerializer,
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def get(self, request, pk):
        try:
            pet = get_object_or_404(Pet, pk=pk)
            serializer = PetReadSerializer(pet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza completamente um pet.",
        request=PetWriteSerializer,
        responses={
            200: PetReadSerializer,
            400: OpenApiResponse(description="Erro de validação"),
        },
    )
    def put(self, request, pk):
        try:
            pet = get_object_or_404(Pet, pk=pk)
            serializer = PetWriteSerializer(pet, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Exclui um pet.",
        responses={
            204: OpenApiResponse(description="Deletado com sucesso"),
            404: OpenApiResponse(description="Não encontrado"),
        },
    )
    def delete(self, request, pk):
        try:
            pet = get_object_or_404(Pet, pk=pk)
            pet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PetHeuristicaView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Aplica a heurística para sugerir pets para o adotante.",
        responses={
            200: PetReadSerializer(many=True),
            400: OpenApiResponse(description="Erro ao aplicar heurística"),
        },
    )
    def get(self, request, id):
        from api.services.heuristicaService import HeuristicaService

        try:
            heuristica_service = HeuristicaService()
            pets_sugeridos = heuristica_service.aplicar_heuristica(id_adotante=id)

            serializer = PetScoreSerializer(pets_sugeridos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class PetPorTutorView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        description="Lista todos os pets de um tutor específico.",
        responses={200: PetReadSerializer(many=True)},
    )
    def get(self, request, tutor_id):
        try:
            pets = Pet.objects.filter(tutor_id=tutor_id)
            serializer = PetReadSerializer(pets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

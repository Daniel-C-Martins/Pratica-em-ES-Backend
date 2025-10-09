from api.models.racasPet import RacasPet
from api.serializers.racasPetSerializer import (
    RacasPetReadSerializer,
    RacasPetWriteSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class RacasPetView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            racas_pet = RacasPet.objects.all()
            serializer = RacasPetReadSerializer(racas_pet, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = RacasPetWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RacasPetDetailView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            racas_pet = get_object_or_404(RacasPet, pk=pk)
            serializer = RacasPetReadSerializer(racas_pet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            racas_pet = get_object_or_404(RacasPet, pk=pk)
            serializer = RacasPetWriteSerializer(racas_pet, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            racas_pet = get_object_or_404(RacasPet, pk=pk)
            racas_pet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

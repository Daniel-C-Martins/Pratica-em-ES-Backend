from api.models.especiePet import EspeciePet
from api.serialiazers.especiePetSerializer import (
    EspeciePetReadSerializer,
    EspeciePetWriteSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class EspeciePetView(APIView):
    def get(self, request):
        try:
            especies = EspeciePet.objects.all()
            serializer = EspeciePetReadSerializer(especies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = EspeciePetWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EspeciePetDetailView(APIView):
    def get(self, request, pk):
        try:
            especie = get_object_or_404(EspeciePet, pk=pk)
            serializer = EspeciePetReadSerializer(especie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            especie = get_object_or_404(EspeciePet, pk=pk)
            serializer = EspeciePetWriteSerializer(especie, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            especie = get_object_or_404(EspeciePet, pk=pk)
            especie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

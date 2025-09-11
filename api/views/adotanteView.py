from api.models.adotante import Adotante
from api.serialiazers.adotanteSerializer import (
    AdotanteReadSerializer,
    AdotanteWriteSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class AdotanteView(APIView):
    def get(self, request):
        try:
            adotantes = Adotante.objects.all()
            serializer = AdotanteReadSerializer(adotantes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = AdotanteWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdotanteDetailView(APIView):
    def get(self, request, pk):
        try:
            adotante = get_object_or_404(Adotante, pk=pk)
            serializer = AdotanteReadSerializer(adotante)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            adotante = get_object_or_404(Adotante, pk=pk)
            serializer = AdotanteWriteSerializer(adotante, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            adotante = get_object_or_404(Adotante, pk=pk)
            adotante.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

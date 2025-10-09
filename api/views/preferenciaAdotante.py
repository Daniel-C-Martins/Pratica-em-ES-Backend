from api.models.preferenciaAdotante import PreferenciaAdotante
from api.serializers.preferenciaAdotanteSerializer import (
    PreferenciaAdotanteReadSerializer,
    PreferenciaAdotanteWriteSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class PreferenciaAdotanteView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            preferencias = PreferenciaAdotante.objects.all()
            serializer = PreferenciaAdotanteReadSerializer(preferencias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

    def get(self, request, pk):
        try:
            preferencia = get_object_or_404(PreferenciaAdotante, pk=pk)
            serializer = PreferenciaAdotanteReadSerializer(preferencia)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            preferencia = get_object_or_404(PreferenciaAdotante, pk=pk)
            serializer = PreferenciaAdotanteWriteSerializer(
                preferencia, data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            preferencia = get_object_or_404(PreferenciaAdotante, pk=pk)
            preferencia.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

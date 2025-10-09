from api.models.adocao import Adocao
from api.serializers.adocaoSerializer import (
    AdocaoReadSerializer,
    AdocaoWriteSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class AdocaoView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            adocoes = Adocao.objects.all()
            serializer = AdocaoReadSerializer(adocoes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = AdocaoWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdocaoDetailView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            adocao = get_object_or_404(Adocao, pk=pk)
            serializer = AdocaoReadSerializer(adocao)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            adocao = get_object_or_404(Adocao, pk=pk)
            serializer = AdocaoWriteSerializer(adocao, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            adocao = get_object_or_404(Adocao, pk=pk)
            adocao.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

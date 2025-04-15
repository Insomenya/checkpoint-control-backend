from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Zone, Checkpoint
from .serializers import ZoneSerializer, CheckpointSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class CheckpointViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления КПП.
    """
    queryset = Checkpoint.objects.all()
    serializer_class = CheckpointSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @swagger_auto_schema(operation_summary='Получить список КПП')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Получить данные КПП')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Создать новый КПП')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Обновить данные КПП')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Частично обновить данные КПП')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Удалить КПП')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

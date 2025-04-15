from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Confirmation
from checkpoints.models import Checkpoint, Zone
from expeditions.models import Expedition
from .serializers import ConfirmationSerializer, ConfirmationCreateSerializer, ConfirmationWithExpeditionSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from datetime import date

class ConfirmationCreateView(generics.CreateAPIView):
    """
    Создание нового подтверждения экспедиции.
    """
    serializer_class = ConfirmationCreateSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Подтвердить экспедицию')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Добавляем пользователя, который подтверждает экспедицию
        serializer.validated_data['confirmed_by'] = request.user
        
        # Проверяем, что пользователь - оператор КПП
        if request.user.role != 'operator':
            return Response(
                {"error": "Только операторы КПП могут подтверждать экспедиции"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Проверяем, что оператор работает на указанном КПП
        checkpoint_id = request.data.get('checkpoint_id')
        if request.user.checkpoint.id != int(checkpoint_id):
            return Response(
                {"error": "Оператор может подтверждать экспедиции только на своем КПП"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Если статус "подтверждено" и это последняя зона, устанавливаем end_date
        expedition = get_object_or_404(Expedition, id=serializer.validated_data['expedition'].id)
        zone = serializer.validated_data['zone']
        
        # Проверка направления и зоны для завершения экспедиции
        if (serializer.validated_data['status'] == 'confirmed' and 
            ((expedition.direction == 'IN' and zone.id == 3) or 
             (expedition.direction == 'OUT' and zone.id == 1))):
            expedition.end_date = date.today()
            expedition.save()
        
        confirmation = serializer.save()
        
        return Response(
            ConfirmationSerializer(confirmation).data,
            status=status.HTTP_201_CREATED
        )

class ZoneConfirmationsView(generics.ListAPIView):
    """
    Получение списка подтверждений для конкретной зоны.
    """
    serializer_class = ConfirmationWithExpeditionSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить список подтверждений для зоны')
    def get_queryset(self):
        zone_id = self.kwargs['zone_id']
        return Confirmation.objects.filter(zone_id=zone_id).order_by('-confirmed_at')

class CheckpointConfirmationsView(generics.ListAPIView):
    """
    Получение списка подтверждений для конкретного КПП.
    """
    serializer_class = ConfirmationWithExpeditionSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить список подтверждений для КПП')
    def get_queryset(self):
        checkpoint_id = self.kwargs['checkpoint_id']
        checkpoint = get_object_or_404(Checkpoint, id=checkpoint_id)
        return Confirmation.objects.filter(zone=checkpoint.zone).order_by('-confirmed_at')

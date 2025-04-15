from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Good, Expedition, Invoice, InvoiceGood
from checkpoints.models import Checkpoint
from confirmations.models import Confirmation
from .serializers import GoodSerializer, ExpeditionSerializer, ExpeditionListSerializer
from confirmations.serializers import ConfirmationWithExpeditionSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from datetime import date
from django.db.models import Q
from django.utils import timezone

class GoodViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления товарно-материальными ценностями.
    """
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить список ТМЦ')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Получить данные ТМЦ')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Создать новую ТМЦ')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Обновить данные ТМЦ')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Частично обновить данные ТМЦ')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Удалить ТМЦ')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ExpeditionCreateView(generics.CreateAPIView):
    """
    Создание новой экспедиции с накладными и ТМЦ.
    """
    serializer_class = ExpeditionSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Создать новую экспедицию')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Добавляем пользователя и текущую дату
        serializer.validated_data['created_by'] = request.user
        serializer.validated_data['start_date'] = date.today()
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ExpeditionDetailView(generics.RetrieveAPIView):
    """
    Получение данных экспедиции по ID.
    """
    serializer_class = ExpeditionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Expedition.objects.all()
    
    @swagger_auto_schema(operation_summary='Получить данные экспедиции')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ExpeditionListView(generics.ListAPIView):
    """
    Получение списка всех экспедиций.
    """
    serializer_class = ExpeditionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Expedition.objects.all().order_by('-start_date')
    
    @swagger_auto_schema(operation_summary='Получить список всех экспедиций')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CheckpointExpeditionsView(generics.ListAPIView):
    """
    Получение списка экспедиций для конкретного КПП.
    """
    serializer_class = ExpeditionSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить список экспедиций для КПП')
    def get_queryset(self):
        checkpoint_id = self.kwargs['checkpoint_id']
        checkpoint = get_object_or_404(Checkpoint, id=checkpoint_id)
        zone = checkpoint.zone
        
        # Получаем все экспедиции, которые не имеют подтверждения в текущей зоне,
        # но имеют подтверждение в предыдущей зоне
        if zone.id == 1:  # Первая зона (КПП охраны)
            if self.request.query_params.get('direction') == 'OUT':
                # Для выезда: экспедиции, подтвержденные в зоне 2, но не в зоне 1
                confirmed_in_zone_2 = Confirmation.objects.filter(
                    zone_id=2, 
                    status='confirmed'
                ).values_list('expedition_id', flat=True)
                
                confirmed_in_zone_1 = Confirmation.objects.filter(
                    zone_id=1, 
                    status__in=['confirmed', 'cancelled']
                ).values_list('expedition_id', flat=True)
                
                return Expedition.objects.filter(
                    id__in=confirmed_in_zone_2
                ).exclude(
                    id__in=confirmed_in_zone_1
                ).filter(
                    direction='OUT'
                )
            else:
                # Для въезда: экспедиции без подтверждений в зоне 1
                confirmed_expeditions = Confirmation.objects.filter(
                    status__in=['confirmed', 'cancelled']
                ).values_list('expedition_id', flat=True)
                
                return Expedition.objects.filter(
                    direction='IN'
                ).exclude(
                    id__in=confirmed_expeditions
                )
        
        elif zone.id == 2:  # Вторая зона (Бюро пропусков)
            if self.request.query_params.get('direction') == 'OUT':
                # Для выезда: экспедиции, подтвержденные в зоне 3, но не в зоне 2
                confirmed_in_zone_3 = Confirmation.objects.filter(
                    zone_id=3, 
                    status='confirmed'
                ).values_list('expedition_id', flat=True)
                
                confirmed_in_zone_2 = Confirmation.objects.filter(
                    zone_id=2, 
                    status__in=['confirmed', 'cancelled']
                ).values_list('expedition_id', flat=True)
                
                return Expedition.objects.filter(
                    id__in=confirmed_in_zone_3
                ).exclude(
                    id__in=confirmed_in_zone_2
                ).filter(
                    direction='OUT'
                )
            else:
                # Для въезда: экспедиции, подтвержденные в зоне 1, но не в зоне 2
                confirmed_in_zone_1 = Confirmation.objects.filter(
                    zone_id=1, 
                    status='confirmed'
                ).values_list('expedition_id', flat=True)
                
                confirmed_in_zone_2 = Confirmation.objects.filter(
                    zone_id=2, 
                    status__in=['confirmed', 'cancelled']
                ).values_list('expedition_id', flat=True)
                
                return Expedition.objects.filter(
                    id__in=confirmed_in_zone_1
                ).exclude(
                    id__in=confirmed_in_zone_2
                ).filter(
                    direction='IN'
                )
        
        elif zone.id == 3:  # Третья зона (Склад)
            if self.request.query_params.get('direction') == 'OUT':
                # Для выезда: экспедиции без подтверждений в зоне 3
                all_out_expeditions = Expedition.objects.filter(direction='OUT')
                
                confirmed_in_zone_3 = Confirmation.objects.filter(
                    zone_id=3, 
                    status__in=['confirmed', 'cancelled']
                ).values_list('expedition_id', flat=True)
                
                return all_out_expeditions.exclude(id__in=confirmed_in_zone_3)
            else:
                # Для въезда: экспедиции, подтвержденные в зоне 2, но не в зоне 3
                confirmed_in_zone_2 = Confirmation.objects.filter(
                    zone_id=2, 
                    status='confirmed'
                ).values_list('expedition_id', flat=True)
                
                confirmed_in_zone_3 = Confirmation.objects.filter(
                    zone_id=3, 
                    status__in=['confirmed', 'cancelled']
                ).values_list('expedition_id', flat=True)
                
                return Expedition.objects.filter(
                    id__in=confirmed_in_zone_2
                ).exclude(
                    id__in=confirmed_in_zone_3
                ).filter(
                    direction='IN'
                )
        
        return Expedition.objects.none()

class CheckpointExpeditionsIdsView(generics.ListAPIView):
    """
    Получение списка ID экспедиций для конкретного КПП.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить список ID экспедиций для КПП')
    def get(self, request, checkpoint_id):
        checkpoint = get_object_or_404(Checkpoint, id=checkpoint_id)
        
        # Используем ту же логику, что и в CheckpointExpeditionsView
        view = CheckpointExpeditionsView()
        view.kwargs = {'checkpoint_id': checkpoint_id}
        view.request = request
        
        queryset = view.get_queryset()
        expedition_ids = queryset.values_list('id', flat=True)
        
        return Response({'expedition_ids': list(expedition_ids)})

class ExpeditionStatusView(generics.RetrieveAPIView):
    """
    Получение статуса экспедиции.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить статус экспедиции')
    def get(self, request, expedition_id):
        expedition = get_object_or_404(Expedition, id=expedition_id)
        
        # Получаем последнее подтверждение для экспедиции
        last_confirmation = Confirmation.objects.filter(
            expedition=expedition
        ).order_by('-confirmed_at').first()
        
        # Сериализуем экспедицию
        expedition_serializer = ExpeditionSerializer(expedition)
        response_data = expedition_serializer.data
        
        # Добавляем данные о подтверждении, если оно есть
        if last_confirmation:
            confirmation_serializer = ConfirmationWithExpeditionSerializer(last_confirmation)
            response_data['last_confirmation'] = confirmation_serializer.data
        else:
            response_data['last_confirmation'] = None
        
        return Response(response_data)

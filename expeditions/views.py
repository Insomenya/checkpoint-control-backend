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
from drf_yasg import openapi
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
    
    @swagger_auto_schema(
        operation_summary='Создать новую экспедицию',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'direction', 'sender_id', 'receiver_id', 'type', 'full_name', 'phone_number'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Наименование экспедиции'),
                'direction': openapi.Schema(type=openapi.TYPE_STRING, enum=['IN', 'OUT'], description='Направление (IN - въезд, OUT - выезд)'),
                'sender_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID организации-отправителя'),
                'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID организации-получателя'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['auto', 'selfauto', 'selfout'], description='Тип экспедиции'),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='ФИО водителя/представителя'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Номер телефона'),
                'license_plate': openapi.Schema(type=openapi.TYPE_STRING, description='Гос. номер ТС (для auto и selfauto)'),
                'vehicle_model': openapi.Schema(type=openapi.TYPE_STRING, description='Модель ТС (для auto и selfauto)'),
                'passport_number': openapi.Schema(type=openapi.TYPE_STRING, description='Номер паспорта'),
                'invoices': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description='Список накладных с товарами',
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['number', 'cargo_description', 'goods'],
                        properties={
                            'number': openapi.Schema(type=openapi.TYPE_STRING, description='Номер накладной'),
                            'cargo_description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание груза'),
                            'goods': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    required=['name'],
                                    properties={
                                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название ТМЦ'),
                                        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание ТМЦ'),
                                        'unit_of_measurement': openapi.Schema(type=openapi.TYPE_STRING, enum=['шт', 'кг', 'л', 'м'], description='Единица измерения'),
                                        'quantity': openapi.Schema(type=openapi.TYPE_NUMBER, description='Количество (по умолчанию: 1)')
                                    }
                                )
                            )
                        }
                    )
                )
            }
        )
    )
    def post(self, request, *args, **kwargs):
        # Преобразуем данные о накладных в правильный формат
        data = request.data.copy()
        if 'invoices' in data:
            data['invoices_data'] = data.pop('invoices')
        
        serializer = self.get_serializer(data=data)
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

class ExpeditionsStatusView(generics.ListAPIView):
    """
    Получение статусов всех экспедиций.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить статусы всех экспедиций')
    def get(self, request):
        expeditions = Expedition.objects.all()
        result = []
        
        for expedition in expeditions:
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
            
            result.append(response_data)
        
        return Response(result)

class CheckpointExpeditionsStatusView(generics.ListAPIView):
    """
    Получение статусов экспедиций для конкретного КПП, которые ожидают подтверждения.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить статусы экспедиций для КПП')
    def get(self, request, checkpoint_id):
        checkpoint = get_object_or_404(Checkpoint, id=checkpoint_id)
        zone = checkpoint.zone
        result = []
        
        # Вместо использования CheckpointExpeditionsView, реализуем отдельную логику без учета параметра direction
        # Для въезда: зоны идут в порядке 1 -> 2 -> 3
        # Для выезда: зоны идут в порядке 3 -> 2 -> 1
        
        # Экспедиции на въезд (IN)
        in_expeditions = Expedition.objects.filter(direction='IN')
        
        # Экспедиции на выезд (OUT)
        out_expeditions = Expedition.objects.filter(direction='OUT')
        
        if zone.id == 1:  # Первая зона (КПП охраны)
            # Для выезда (OUT): экспедиции, подтвержденные в зоне 2, но не в зоне 1
            confirmed_in_zone_2 = Confirmation.objects.filter(
                zone_id=2, 
                status='confirmed'
            ).values_list('expedition_id', flat=True)
            
            confirmed_in_zone_1 = Confirmation.objects.filter(
                zone_id=1, 
                status__in=['confirmed', 'cancelled']
            ).values_list('expedition_id', flat=True)
            
            out_pending = out_expeditions.filter(
                id__in=confirmed_in_zone_2
            ).exclude(
                id__in=confirmed_in_zone_1
            )
            
            # Для въезда (IN): экспедиции без подтверждений в зоне 1
            all_confirmed_in_zone_1 = Confirmation.objects.filter(
                zone_id=1,
                status__in=['confirmed', 'cancelled']
            ).values_list('expedition_id', flat=True)
            
            in_pending = in_expeditions.exclude(
                id__in=all_confirmed_in_zone_1
            )
            
            pending_expeditions = list(in_pending) + list(out_pending)
            
        elif zone.id == 2:  # Вторая зона (Бюро пропусков)
            # Для выезда (OUT): экспедиции, подтвержденные в зоне 3, но не в зоне 2
            confirmed_in_zone_3 = Confirmation.objects.filter(
                zone_id=3, 
                status='confirmed'
            ).values_list('expedition_id', flat=True)
            
            confirmed_in_zone_2 = Confirmation.objects.filter(
                zone_id=2, 
                status__in=['confirmed', 'cancelled']
            ).values_list('expedition_id', flat=True)
            
            out_pending = out_expeditions.filter(
                id__in=confirmed_in_zone_3
            ).exclude(
                id__in=confirmed_in_zone_2
            )
            
            # Для въезда (IN): экспедиции, подтвержденные в зоне 1, но не в зоне 2
            confirmed_in_zone_1 = Confirmation.objects.filter(
                zone_id=1, 
                status='confirmed'
            ).values_list('expedition_id', flat=True)
            
            confirmed_in_zone_2_in = Confirmation.objects.filter(
                zone_id=2, 
                status__in=['confirmed', 'cancelled']
            ).values_list('expedition_id', flat=True)
            
            in_pending = in_expeditions.filter(
                id__in=confirmed_in_zone_1
            ).exclude(
                id__in=confirmed_in_zone_2_in
            )
            
            pending_expeditions = list(in_pending) + list(out_pending)
            
        elif zone.id == 3:  # Третья зона (Склад)
            # Для выезда (OUT): экспедиции без подтверждений в зоне 3
            confirmed_in_zone_3 = Confirmation.objects.filter(
                zone_id=3, 
                status__in=['confirmed', 'cancelled']
            ).values_list('expedition_id', flat=True)
            
            out_pending = out_expeditions.exclude(id__in=confirmed_in_zone_3)
            
            # Для въезда (IN): экспедиции, подтвержденные в зоне 2, но не в зоне 3
            confirmed_in_zone_2 = Confirmation.objects.filter(
                zone_id=2, 
                status='confirmed'
            ).values_list('expedition_id', flat=True)
            
            confirmed_in_zone_3_in = Confirmation.objects.filter(
                zone_id=3, 
                status__in=['confirmed', 'cancelled']
            ).values_list('expedition_id', flat=True)
            
            in_pending = in_expeditions.filter(
                id__in=confirmed_in_zone_2
            ).exclude(
                id__in=confirmed_in_zone_3_in
            )
            
            pending_expeditions = list(in_pending) + list(out_pending)
        else:
            pending_expeditions = []
        
        for expedition in pending_expeditions:
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
            
            result.append(response_data)
        
        return Response(result)

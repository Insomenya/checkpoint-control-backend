from rest_framework import serializers
from .models import Good, Expedition, Invoice, InvoiceGood
from organizations.serializers import OrganizationSerializer
from organizations.models import Organization

class GoodSerializer(serializers.ModelSerializer):
    unit_of_measurement_display = serializers.CharField(source='get_unit_of_measurement_display', read_only=True)
    
    class Meta:
        model = Good
        fields = ['id', 'name', 'description', 'unit_of_measurement', 'unit_of_measurement_display']

class InvoiceGoodSerializer(serializers.ModelSerializer):
    good = GoodSerializer()
    
    class Meta:
        model = InvoiceGood
        fields = ['id', 'good', 'quantity']

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_goods = InvoiceGoodSerializer(many=True, read_only=True)
    goods = serializers.ListField(write_only=True, required=False)
    
    class Meta:
        model = Invoice
        fields = ['id', 'number', 'cargo_description', 'invoice_goods', 'goods']

    def create(self, validated_data):
        goods_data = validated_data.pop('goods', [])
        invoice = Invoice.objects.create(**validated_data)
        
        for good_data in goods_data:
            good_instance, _ = Good.objects.get_or_create(
                name=good_data['name'],
                defaults={
                    'description': good_data.get('description', ''),
                    'unit_of_measurement': good_data.get('unit_of_measurement', 'шт')
                }
            )
            
            InvoiceGood.objects.create(
                invoice=invoice,
                good=good_instance,
                quantity=good_data.get('quantity', 1)
            )
        
        return invoice

class ExpeditionSerializer(serializers.ModelSerializer):
    invoices = InvoiceSerializer(many=True, read_only=True)
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.name', read_only=True)
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    sender_id = serializers.IntegerField(write_only=True)
    receiver_id = serializers.IntegerField(write_only=True)
    invoices_data = serializers.ListField(write_only=True, required=False)
    
    class Meta:
        model = Expedition
        fields = [
            'id', 'name', 'direction', 'direction_display', 
            'type', 'type_display', 'sender_id', 'sender_name', 
            'receiver_id', 'receiver_name', 'created_by', 
            'full_name', 'passport_number', 'phone_number', 
            'license_plate', 'vehicle_model', 'start_date', 
            'end_date', 'invoices', 'sender_id', 'receiver_id',
            'invoices_data'
        ]
        read_only_fields = ['created_by', 'start_date', 'end_date']
    
    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        receiver_id = validated_data.pop('receiver_id')
        
        sender = Organization.objects.get(id=sender_id)
        receiver = Organization.objects.get(id=receiver_id)
        
        invoices_data = validated_data.pop('invoices_data', [])
        
        expedition = Expedition.objects.create(
            sender=sender,
            receiver=receiver,
            **validated_data
        )
        
        for invoice_data in invoices_data:
            goods_data = invoice_data.pop('goods', [])
            invoice = Invoice.objects.create(expedition=expedition, **invoice_data)
            
            for good_data in goods_data:
                good, _ = Good.objects.get_or_create(
                    name=good_data['name'],
                    defaults={
                        'description': good_data.get('description', ''),
                        'unit_of_measurement': good_data.get('unit_of_measurement', 'шт')
                    }
                )
                
                InvoiceGood.objects.create(
                    invoice=invoice,
                    good=good,
                    quantity=good_data.get('quantity', 1)
                )
        
        return expedition

class ExpeditionListSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.name', read_only=True)
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Expedition
        fields = [
            'id', 'name', 'direction', 'direction_display',
            'type', 'type_display', 'sender_id', 'sender_name', 'receiver_id', 'receiver_name',
            'full_name', 'start_date'
        ] 
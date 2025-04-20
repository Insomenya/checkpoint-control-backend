from rest_framework import serializers
from .models import Confirmation
from checkpoints.models import Checkpoint, Zone
from expeditions.models import Expedition

class ExpeditionMinimalSerializer(serializers.Serializer):
    """Минимальная информация об экспедиции для вложения в подтверждение"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    direction = serializers.CharField()
    type = serializers.CharField()
    direction_display = serializers.CharField(source='get_direction_display')
    type_display = serializers.CharField(source='get_type_display')

class ConfirmationSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    confirmed_by_username = serializers.CharField(source='confirmed_by.username', read_only=True)
    
    class Meta:
        model = Confirmation
        fields = ['id', 'expedition_id', 'confirmed_by', 'confirmed_by_username', 'zone_id', 'zone_name', 'status', 'status_display', 'confirmed_at']
        read_only_fields = ['confirmed_by', 'confirmed_at']

class ConfirmationCreateSerializer(serializers.ModelSerializer):
    checkpoint_id = serializers.IntegerField(write_only=True)
    expedition_id = serializers.IntegerField(required=True, write_only=True)
    
    class Meta:
        model = Confirmation
        fields = ['expedition_id', 'checkpoint_id', 'status']
    
    def validate(self, attrs):
        expedition_id = attrs.get('expedition_id')
        try:
            Expedition.objects.get(id=expedition_id)
        except Expedition.DoesNotExist:
            raise serializers.ValidationError({"expedition_id": "Экспедиция не найдена"})
        
        checkpoint_id = attrs.pop('checkpoint_id')
        checkpoint = Checkpoint.objects.get(id=checkpoint_id)
        attrs['zone'] = checkpoint.zone
        return attrs
    
    def create(self, validated_data):
        expedition_id = validated_data.pop('expedition_id')
        expedition = Expedition.objects.get(id=expedition_id)
        
        return Confirmation.objects.create(
            expedition=expedition,
            **validated_data
        )

class ConfirmationWithExpeditionSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    confirmed_by_username = serializers.CharField(source='confirmed_by.username', read_only=True)
    expedition = ExpeditionMinimalSerializer(read_only=True)
    
    class Meta:
        model = Confirmation
        fields = ['id', 'expedition', 'confirmed_by', 'confirmed_by_username', 'zone_id', 'zone_name', 'status', 'status_display', 'confirmed_at'] 
from rest_framework import serializers
from .models import Confirmation
from checkpoints.models import Checkpoint, Zone

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
        fields = ['id', 'expedition', 'confirmed_by', 'confirmed_by_username', 'zone', 'zone_name', 'status', 'status_display', 'confirmed_at']
        read_only_fields = ['confirmed_by', 'confirmed_at']

class ConfirmationCreateSerializer(serializers.ModelSerializer):
    checkpoint_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Confirmation
        fields = ['expedition', 'checkpoint_id', 'status']
    
    def validate(self, attrs):
        checkpoint_id = attrs.pop('checkpoint_id')
        checkpoint = Checkpoint.objects.get(id=checkpoint_id)
        attrs['zone'] = checkpoint.zone
        return attrs
    
    def create(self, validated_data):
        # Поле confirmed_by будет установлено в представлении
        return Confirmation.objects.create(**validated_data)

class ConfirmationWithExpeditionSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    confirmed_by_username = serializers.CharField(source='confirmed_by.username', read_only=True)
    expedition = ExpeditionMinimalSerializer(read_only=True)
    
    class Meta:
        model = Confirmation
        fields = ['id', 'expedition', 'confirmed_by', 'confirmed_by_username', 'zone', 'zone_name', 'status', 'status_display', 'confirmed_at'] 
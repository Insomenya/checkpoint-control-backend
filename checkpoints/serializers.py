from rest_framework import serializers
from .models import Zone, Checkpoint

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class CheckpointSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    
    class Meta:
        model = Checkpoint
        fields = ['id', 'name', 'zone_id', 'zone_name'] 
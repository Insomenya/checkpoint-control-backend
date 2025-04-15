from rest_framework import serializers
from django.contrib.auth import get_user_model
from checkpoints.models import Checkpoint

User = get_user_model()

class CheckpointMinimalSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class UserDetailSerializer(serializers.ModelSerializer):
    checkpoint = CheckpointMinimalSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'role_display', 'checkpoint']
        read_only_fields = ['id', 'username', 'role', 'role_display', 'checkpoint']

class UserSignupSerializer(serializers.ModelSerializer):
    checkpoint_id = serializers.IntegerField(required=False, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'role', 'checkpoint_id']
    
    def validate(self, attrs):
        role = attrs.get('role')
        checkpoint_id = attrs.get('checkpoint_id')
        
        if role == 'operator' and not checkpoint_id:
            raise serializers.ValidationError({'checkpoint_id': 'Для оператора необходимо указать КПП'})
        
        return attrs
    
    def create(self, validated_data):
        checkpoint_id = validated_data.pop('checkpoint_id', None)
        
        if checkpoint_id:
            checkpoint = Checkpoint.objects.get(id=checkpoint_id)
            user = User.objects.create_user(
                username=validated_data['username'],
                role=validated_data['role'],
                checkpoint=checkpoint
            )
        else:
            user = User.objects.create_user(
                username=validated_data['username'],
                role=validated_data['role']
            )
        
        return user

class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен содержать не менее 8 символов")
        return value

class UserListSerializer(serializers.ModelSerializer):
    checkpoint_name = serializers.CharField(source='checkpoint.name', read_only=True, allow_null=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'role_display', 'checkpoint_id', 'checkpoint_name', 'is_password_set']
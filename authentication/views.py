from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserDetailSerializer, UserSignupSerializer, SetPasswordSerializer, UserListSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
import uuid

User = get_user_model()

# Хранение временных токенов для сброса пароля
# В реальном проекте лучше использовать Redis или другое хранилище
USER_TOKENS = {}

class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить данные текущего пользователя')
    def get_object(self):
        return self.request.user

class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @swagger_auto_schema(operation_summary='Зарегистрировать нового пользователя')
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            # Генерируем уникальный токен для установки пароля
            token = str(uuid.uuid4())
            USER_TOKENS[token] = user.id
            
            return Response(
                {"signup_link": f"/auth/setpass/{token}"},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetPasswordView(generics.GenericAPIView):
    serializer_class = SetPasswordSerializer
    
    @swagger_auto_schema(operation_summary='Установить пароль при первом входе')
    def post(self, request, token):
        user_id = USER_TOKENS.get(token)
        
        if not user_id:
            return Response(
                {"error": "Неверная ссылка для установки пароля или срок ее действия истек"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = get_object_or_404(User, id=user_id)
            
            if user.is_password_set:
                return Response(
                    {"error": "Пароль уже установлен для этого пользователя"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['password'])
            user.is_password_set = True
            user.save()
            
            # Удаляем использованный токен
            USER_TOKENS.pop(token)
            
            return Response(
                {"message": "Пароль успешно установлен"},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    
    @swagger_auto_schema(operation_summary='Получить список пользователей')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserDetailSerializer, UserSignupSerializer, SetPasswordSerializer, UserListSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from drf_yasg import openapi

User = get_user_model()

class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(operation_summary='Получить данные текущего пользователя')
    def get_object(self):
        return self.request.user

class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @swagger_auto_schema(
        operation_summary='Зарегистрировать нового пользователя',
        responses={
            201: openapi.Response(
                description="Пользователь успешно создан",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID созданного пользователя'),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Токен для установки пароля'),
                        'signup_link': openapi.Schema(type=openapi.TYPE_STRING, description='Полная ссылка для установки пароля')
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            # Генерируем уникальный токен для установки пароля
            token = user.generate_password_reset_token()
            
            # Получаем хост из запроса для формирования полного URL
            protocol = 'https' if request.is_secure() else 'http'
            host = request.get_host()
            
            return Response({
                "user_id": user.id,
                "username": user.username,
                "token": token,
                "signup_link": f"{protocol}://{host}/auth/setpass/{token}"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetPasswordView(generics.GenericAPIView):
    serializer_class = SetPasswordSerializer
    
    @swagger_auto_schema(
        operation_summary='Установить пароль при первом входе',
        request_body=SetPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Пароль успешно установлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Сообщение об успешной установке пароля')
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка в запросе",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Описание ошибки')
                    }
                )
            ),
            404: "Токен не найден"
        }
    )
    def post(self, request, token):
        # Ищем пользователя по токену
        user = get_object_or_404(User, password_reset_token=token)
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            if user.is_password_set:
                return Response(
                    {"error": "Пароль уже установлен для этого пользователя"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['password'])
            user.is_password_set = True
            # Очищаем токен, чтобы его нельзя было использовать повторно
            user.clear_password_reset_token()
            
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
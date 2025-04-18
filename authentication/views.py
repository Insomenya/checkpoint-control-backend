from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserDetailSerializer, UserSignupSerializer, SetPasswordSerializer, UserListSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from drf_yasg import openapi
from django.conf import settings
import logging
from django.db.models import Count
from .models import User

# Получаем логгер для приложения authentication
logger = logging.getLogger(__name__)

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
            
            # Используем Origin или Referer заголовок для определения хоста фронтенда
            if 'Origin' in request.headers:
                # Получаем хост фронтенда из заголовка Origin
                frontend_url = request.headers['Origin']
                logger.debug(f"Using Origin header for frontend URL: {frontend_url}")
            elif 'Referer' in request.headers:
                # Если Origin нет, пробуем использовать Referer
                frontend_url = request.headers['Referer']
                # Удаляем путь из URL, если он есть (оставляем только домен)
                frontend_url = frontend_url.split('/', 3)[0] + '//' + frontend_url.split('/', 3)[2]
                logger.debug(f"Using Referer header for frontend URL: {frontend_url}")
            else:
                # Если ни Origin, ни Referer не предоставлены, используем хост бэкенда (как было раньше)
                protocol = 'https' if request.is_secure() else 'http'
                frontend_url = f"{protocol}://{request.get_host()}"
                logger.debug(f"Using backend host for frontend URL: {frontend_url}")
            
            # Получаем путь к странице установки пароля из настроек
            password_setup_path = getattr(settings, 'FRONTEND_PASSWORD_SETUP_PATH', '/auth/setpass/')
            
            # Формируем полную ссылку с хостом фронтенда
            signup_link = f"{frontend_url}{password_setup_path}{token}"
            logger.info(f"User {user.username} created with signup link: {signup_link}")
            
            return Response({
                "user_id": user.id,
                "username": user.username,
                "token": token,
                "signup_link": signup_link
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
        try:
            user = get_object_or_404(User, password_reset_token=token)
            logger.debug(f"Found user {user.username} for password reset token")
            
            serializer = self.serializer_class(data=request.data)
            
            if serializer.is_valid():
                if user.is_password_set:
                    logger.warning(f"User {user.username} already has password set")
                    return Response(
                        {"error": "Пароль уже установлен для этого пользователя"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Устанавливаем пароль
                user.set_password(serializer.validated_data['password'])
                # Устанавливаем флаг, что пароль установлен
                user.is_password_set = True
                # Сохраняем изменения пользователя
                user.save(update_fields=['password', 'is_password_set'])
                logger.info(f"Password set for user {user.username}")
                
                # Очищаем токен, чтобы его нельзя было использовать повторно
                user.clear_password_reset_token()
                logger.debug(f"Password reset token cleared for user {user.username}")
                
                return Response(
                    {"message": "Пароль успешно установлен"},
                    status=status.HTTP_200_OK
                )
            
            logger.warning(f"Invalid serializer data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error setting password with token {token}: {str(e)}")
            raise

class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    
    @swagger_auto_schema(operation_summary='Получить список пользователей')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Получить статистику по пользователям',
        responses={
            200: openapi.Response(
                description="Статистика по пользователям",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_users': openapi.Schema(type=openapi.TYPE_INTEGER, description='Общее количество пользователей'),
                        'users_by_role': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            description='Количество пользователей по ролям',
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'role': openapi.Schema(type=openapi.TYPE_STRING, description='Название роли'),
                                    'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество пользователей')
                                }
                            )
                        ),
                        'password_set_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество пользователей, установивших пароль'),
                        'password_not_set_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество пользователей, не установивших пароль'),
                        'operators_without_checkpoint_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество операторов без назначенного КПП')
                    }
                )
            )
        }
    )
    def get(self, request):
        total_users = User.objects.count()
        
        users_by_role = User.objects.values('role').annotate(count=Count('role')).order_by('role')
        roles_dict = dict(User.ROLES)
        users_by_role_display = [{'role': roles_dict.get(item['role'], item['role']), 'count': item['count']} for item in users_by_role]
        
        password_set_count = User.objects.filter(is_password_set=True).count()
        password_not_set_count = total_users - password_set_count
        
        operators_without_checkpoint_count = User.objects.filter(role='operator', checkpoint__isnull=True).count()

        stats = {
            'total_users': total_users,
            'users_by_role': users_by_role_display,
            'password_set_count': password_set_count,
            'password_not_set_count': password_not_set_count,
            'operators_without_checkpoint_count': operators_without_checkpoint_count
        }
        return Response(stats)
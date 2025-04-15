from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.crypto import get_random_string

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_("Необходимо указать имя пользователя"))
        
        user = self.model(username=username, **extra_fields)
        
        if password:
            user.set_password(password)
            user.is_password_set = True
        else:
            user.is_password_set = False
            
        user.save()
        return user
    
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_password_set', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Админ должен иметь is_staff = true"))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Админ должен иметь is_superuser = true"))
        
        if extra_fields.get('is_active') is not True:
            raise ValueError(_("Админ должен иметь is_active = true"))
        
        return self.create_user(username, password, **extra_fields)

class User(AbstractUser):
    ROLES = (
        ('logistician', 'Логист'),
        ('operator', 'Оператор'),
        ('admin', 'Администратор')
    )
    
    username = models.CharField("Имя пользователя", max_length=255, unique=True)
    role = models.CharField("Роль", max_length=50, choices=ROLES, default=ROLES[0][0])
    is_password_set = models.BooleanField("Пароль установлен", default=False)
    checkpoint = models.ForeignKey('checkpoints.Checkpoint', verbose_name="КПП", on_delete=models.SET_NULL, null=True, blank=True)
    
    # Устанавливаем поле email и phone_number как необязательные
    email = models.EmailField(_("Email"), blank=True, null=True)
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    objects = CustomUserManager()

    def __str__(self):
        return f"Пользователь {self.username} ({self.get_role_display()})"
    
    def generate_signup_link(self):
        """Генерирует уникальную ссылку для регистрации пользователя"""
        token = get_random_string(length=32)
        return token
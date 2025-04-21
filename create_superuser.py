import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkpoint_control.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        role='admin',
        password='admin123'
    )
    print("Суперпользователь успешно создан:")
    print("Логин: admin")
    print("Пароль: admin123")
else:
    print("Суперпользователь с именем 'admin' уже существует.") 
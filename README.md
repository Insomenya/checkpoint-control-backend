# Система контроля КПП

API для системы контроля движения ТМЦ (товарно-материальных ценностей) через КПП предприятия.

## Основные возможности

* Регистрация экспедиций (въезд/выезд)
* Управление накладными и ТМЦ
* Подтверждение экспедиций на КПП
* Поддержка ролей пользователей (логист, оператор КПП, администратор)
* API документация с использованием Swagger

## Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/checkpoint-control-backend.git
cd checkpoint-control-backend
```

Создайте виртуальное окружение Python и активируйте его:

```bash
python -m venv ./env

# Для Windows
env\Scripts\activate

# Для Linux/Mac
source env/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка

1. Создайте файл `.env` в корневой директории проекта со следующим содержимым:

```
SECRET_KEY=your-secret-key
DEBUG=True
```

2. Выполните миграции для создания структуры базы данных:

```bash
python manage.py makemigrations authentication
python manage.py makemigrations organizations checkpoints expeditions confirmations
python manage.py migrate
```

> **Примечание**: При возникновении ошибки с несогласованностью миграций (InconsistentMigrationHistory), рекомендуется удалить файл базы данных `db.sqlite3` и выполнить миграции заново.

3. Загрузите начальные данные для зон:

```bash
python manage.py loaddata fixtures/zones.json
```

4. Создайте суперпользователя для доступа к панели администратора:

```bash
python manage.py createsuperuser
```

Если команда выше вызывает ошибки, можно создать суперпользователя через скрипт:

```bash
# Создайте файл create_superuser.py с содержимым:
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkpoint_control.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Создаем суперпользователя
User.objects.create_superuser(
    username='admin',
    role='admin',
    password='admin123'
)
print("Суперпользователь успешно создан: admin/admin123")

# Запустите скрипт
python create_superuser.py
```

## Запуск

Для запуска сервера выполните:

```bash
python manage.py runserver
```

После запуска сервер будет доступен по адресу: http://127.0.0.1:8000/

## Документация API

После запуска сервера документация API доступна по адресам:
- Swagger: http://127.0.0.1:8000/docs/
- ReDoc: http://127.0.0.1:8000/redoc/

## Основные компоненты

1. **Авторизация** 
   - Управление пользователями и доступом с разными ролями
   - JWT аутентификация
   - Создание пользователей администратором и установка паролей через уникальную ссылку

2. **Организации** 
   - Управление информацией об организациях-отправителях и получателях

3. **КПП и зоны** 
   - Управление КПП и зонами предприятия (КПП охраны, Бюро пропусков, Склад)

4. **Экспедиции** 
   - Управление экспедициями с указанием направления движения (въезд/выезд)
   - Регистрация накладных и ТМЦ в составе экспедиции

5. **Подтверждения** 
   - Подтверждение экспедиций операторами КПП
   - Отслеживание статуса подтверждений

## API Endpoints

### Аутентификация
- `POST /auth/jwt/create` - Получение JWT токена
- `POST /auth/jwt/refresh` - Обновление токена
- `POST /auth/jwt/verify` - Проверка токена
- `GET /auth/details` - Получение данных пользователя
- `POST /auth/signup` - Регистрация нового пользователя (только для админов)
- `POST /auth/setpass/<token>` - Установка пароля при первом входе
- `GET /auth/users` - Получение списка пользователей

### Организации
- `GET /orgs/` - Получение списка организаций
- `POST /orgs/` - Создание организации
- `GET /orgs/{id}/` - Получение данных организации
- `PUT/PATCH /orgs/{id}/` - Обновление организации
- `DELETE /orgs/{id}/` - Удаление организации

### КПП
- `GET /checkpoints/` - Получение списка КПП
- `POST /checkpoints/` - Создание КПП
- `GET /checkpoints/{id}/` - Получение данных КПП
- `PUT/PATCH /checkpoints/{id}/` - Обновление КПП
- `DELETE /checkpoints/{id}/` - Удаление КПП

### Экспедиции и ТМЦ
- `GET /goods/` - Получение списка ТМЦ
- `POST /expedition` - Создание экспедиции
- `GET /expedition/{id}` - Получение данных экспедиции
- `GET /expeditions` - Получение списка всех экспедиций
- `GET /expeditions/{checkpoint_id}` - Получение списка экспедиций для КПП
- `GET /expeditions/brief/{checkpoint_id}` - Получение ID экспедиций для КПП
- `GET /expedition/status/{id}` - Получение статуса экспедиции

### Подтверждения
- `POST /confirm` - Подтверждение экспедиции
- `GET /confirmed/zone/{zone_id}` - Получение списка подтверждений для зоны
- `GET /confirmed/checkpoint/{checkpoint_id}` - Получение списка подтверждений для КПП


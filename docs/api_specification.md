# Спецификация API Системы контроля КПП

**Версия:** v1  
**Описание:** REST API для системы контроля КПП.  
**Контакт:** admin@checkpoint-control.com  
**Лицензия:** MIT License

## Содержание
- [Аутентификация](#аутентификация)
- [Пользователи](#пользователи)
- [Организации](#организации)
- [КПП](#кпп)
- [Экспедиции](#экспедиции)
- [Товары](#товары)
- [Подтверждения](#подтверждения)

## Аутентификация

### Получение токена JWT

**Endpoint:** `POST /auth/jwt/create/`

**Описание:** Создание токена JWT для аутентификации.

**Тело запроса:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Ответ (200):**
```json
{
  "access": "string",
  "refresh": "string"
}
```

### Обновление токена JWT

**Endpoint:** `POST /auth/jwt/refresh/`

**Описание:** Обновление токена JWT.

**Тело запроса:**
```json
{
  "refresh": "string"
}
```

**Ответ (200):**
```json
{
  "access": "string"
}
```

### Проверка токена JWT

**Endpoint:** `POST /auth/jwt/verify/`

**Описание:** Проверка валидности токена JWT.

**Тело запроса:**
```json
{
  "token": "string"
}
```

**Ответ (200):** Пустой ответ при успешной проверке

## Пользователи

### Получение данных текущего пользователя

**Endpoint:** `GET /auth/details`

**Описание:** Получение данных аутентифицированного пользователя.

**Ответ (200):**
```json
{
  "id": 1,
  "username": "string",
  "role": "string",
  "role_display": "string",
  "checkpoint": {
    "id": 1,
    "name": "string"
  }
}
```

### Регистрация нового пользователя

**Endpoint:** `POST /auth/signup`

**Описание:** Создание нового пользователя (только для администраторов).

**Тело запроса:**
```json
{
  "username": "string",
  "role": "string",
  "checkpoint_id": 1
}
```

**Ответ (201):**
```json
{
  "user_id": 1,
  "username": "string",
  "token": "string",
  "signup_link": "string"
}
```

### Установка пароля для нового пользователя

**Endpoint:** `POST /auth/setpass/{token}`

**Описание:** Установка пароля при первом входе.

**Тело запроса:**
```json
{
  "password": "string"
}
```

**Ответ (200):**
```json
{
  "message": "Пароль успешно установлен"
}
```

**Ответ (400):**
```json
{
  "error": "Описание ошибки"
}
```

**Ответ (404):** Токен не найден

### Получение списка пользователей

**Endpoint:** `GET /auth/users`

**Описание:** Получение списка всех пользователей (только для администраторов).

**Ответ (200):**
```json
[
  {
    "id": 1,
    "username": "string",
    "role": "string",
    "role_display": "string",
    "checkpoint_id": 1,
    "checkpoint_name": "string",
    "is_password_set": true
  }
]
```

## Организации

### Получение списка организаций

**Endpoint:** `GET /orgs/`

**Описание:** Получение списка всех организаций.

**Ответ (200):**
```json
[
  {
    "id": 1,
    "name": "string",
    "address": "string",
    "phone": "string",
    "contact_person": "string"
  }
]
```

### Получение данных организации

**Endpoint:** `GET /orgs/{id}/`

**Описание:** Получение данных конкретной организации.

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "phone": "string",
  "contact_person": "string"
}
```

### Создание новой организации

**Endpoint:** `POST /orgs/`

**Описание:** Создание новой организации.

**Тело запроса:**
```json
{
  "name": "string",
  "address": "string",
  "phone": "string",
  "contact_person": "string"
}
```

**Ответ (201):**
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "phone": "string",
  "contact_person": "string"
}
```

### Обновление данных организации

**Endpoint:** `PUT /orgs/{id}/`

**Описание:** Полное обновление данных организации.

**Тело запроса:**
```json
{
  "name": "string",
  "address": "string",
  "phone": "string",
  "contact_person": "string"
}
```

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "phone": "string",
  "contact_person": "string"
}
```

### Частичное обновление данных организации

**Endpoint:** `PATCH /orgs/{id}/`

**Описание:** Частичное обновление данных организации.

**Тело запроса:**
```json
{
  "name": "string"
}
```

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "phone": "string",
  "contact_person": "string"
}
```

### Удаление организации

**Endpoint:** `DELETE /orgs/{id}/`

**Описание:** Удаление организации.

**Ответ (204):** Нет содержимого

## КПП

### Получение списка КПП

**Endpoint:** `GET /checkpoints/`

**Описание:** Получение списка всех КПП.

**Ответ (200):**
```json
[
  {
    "id": 1,
    "name": "string",
    "address": "string",
    "zone": 1
  }
]
```

### Получение данных КПП

**Endpoint:** `GET /checkpoints/{id}/`

**Описание:** Получение данных конкретного КПП.

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "zone": 1
}
```

### Создание нового КПП

**Endpoint:** `POST /checkpoints/`

**Описание:** Создание нового КПП (только для администраторов).

**Тело запроса:**
```json
{
  "name": "string",
  "address": "string",
  "zone": 1
}
```

**Ответ (201):**
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "zone": 1
}
```

### Обновление данных КПП

**Endpoint:** `PUT /checkpoints/{id}/`

**Описание:** Полное обновление данных КПП (только для администраторов).

**Тело запроса:**
```json
{
  "name": "string",
  "address": "string",
  "zone": 1
}
```

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "zone": 1
}
```

### Частичное обновление данных КПП

**Endpoint:** `PATCH /checkpoints/{id}/`

**Описание:** Частичное обновление данных КПП (только для администраторов).

**Тело запроса:**
```json
{
  "name": "string"
}
```

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "zone": 1
}
```

### Удаление КПП

**Endpoint:** `DELETE /checkpoints/{id}/`

**Описание:** Удаление КПП (только для администраторов).

**Ответ (204):** Нет содержимого

## Экспедиции

### Создание новой экспедиции

**Endpoint:** `POST /expedition`

**Описание:** Создание новой экспедиции с накладными и ТМЦ.

**Тело запроса:**
```json
{
  "name": "string",
  "direction": "IN",
  "sender_id": 1,
  "receiver_id": 1,
  "type": "auto",
  "full_name": "string",
  "phone_number": "string",
  "license_plate": "string",
  "vehicle_model": "string",
  "passport_number": "string",
  "invoices": [
    {
      "number": "string",
      "cargo_description": "string",
      "goods": [
        {
          "name": "string",
          "description": "string",
          "unit_of_measurement": "шт",
          "quantity": 1
        }
      ]
    }
  ]
}
```

**Ответ (201):**
```json
{
  "id": 1,
  "name": "string",
  "direction": "string",
  "direction_display": "string",
  "type": "string",
  "type_display": "string",
  "sender": 1,
  "sender_name": "string",
  "receiver": 1,
  "receiver_name": "string",
  "created_by": 1,
  "full_name": "string",
  "passport_number": "string",
  "phone_number": "string",
  "license_plate": "string",
  "vehicle_model": "string",
  "start_date": "string",
  "end_date": "string",
  "invoices": [
    {
      "id": 1,
      "number": "string",
      "cargo_description": "string",
      "invoice_goods": [
        {
          "id": 1,
          "good": {
            "id": 1,
            "name": "string",
            "description": "string",
            "unit_of_measurement": "шт",
            "unit_of_measurement_display": "string"
          },
          "quantity": 1
        }
      ]
    }
  ]
}
```

### Получение данных экспедиции

**Endpoint:** `GET /expedition/{id}`

**Описание:** Получение данных конкретной экспедиции.

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "direction": "string",
  "direction_display": "string",
  "type": "string",
  "type_display": "string",
  "sender": 1,
  "sender_name": "string",
  "receiver": 1,
  "receiver_name": "string",
  "created_by": 1,
  "full_name": "string",
  "passport_number": "string",
  "phone_number": "string",
  "license_plate": "string",
  "vehicle_model": "string",
  "start_date": "string",
  "end_date": "string",
  "invoices": [
    {
      "id": 1,
      "number": "string",
      "cargo_description": "string",
      "invoice_goods": [
        {
          "id": 1,
          "good": {
            "id": 1,
            "name": "string",
            "description": "string",
            "unit_of_measurement": "шт",
            "unit_of_measurement_display": "string"
          },
          "quantity": 1
        }
      ]
    }
  ]
}
```

### Получение списка всех экспедиций

**Endpoint:** `GET /expeditions`

**Описание:** Получение списка всех экспедиций.

**Ответ (200):**
```json
[
  {
    "id": 1,
    "name": "string",
    "direction": "string",
    "direction_display": "string",
    "type": "string",
    "type_display": "string",
    "sender": 1,
    "sender_name": "string",
    "receiver": 1,
    "receiver_name": "string",
    "created_by": 1,
    "full_name": "string",
    "passport_number": "string",
    "phone_number": "string",
    "license_plate": "string",
    "vehicle_model": "string",
    "start_date": "string",
    "end_date": "string",
    "invoices": []
  }
]
```

### Получение списка экспедиций для КПП

**Endpoint:** `GET /expeditions/{checkpoint_id}`

**Описание:** Получение списка экспедиций для конкретного КПП.

**Параметры запроса:**
- `direction` - Направление (IN/OUT)

**Ответ (200):**
```json
[
  {
    "id": 1,
    "name": "string",
    "direction": "string",
    "direction_display": "string",
    "type": "string",
    "type_display": "string",
    "sender": 1,
    "sender_name": "string",
    "receiver": 1,
    "receiver_name": "string",
    "created_by": 1,
    "full_name": "string",
    "passport_number": "string",
    "phone_number": "string",
    "license_plate": "string",
    "vehicle_model": "string",
    "start_date": "string",
    "end_date": "string",
    "invoices": []
  }
]
```

### Получение списка ID экспедиций для КПП

**Endpoint:** `GET /expeditions/brief/{checkpoint_id}`

**Описание:** Получение списка ID экспедиций для конкретного КПП.

**Параметры запроса:**
- `direction` - Направление (IN/OUT)

**Ответ (200):**
```json
{
  "expedition_ids": [1, 2, 3]
}
```

### Получение статуса экспедиции

**Endpoint:** `GET /expedition/status/{expedition_id}`

**Описание:** Получение статуса конкретной экспедиции, включая последнее подтверждение.

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "direction": "string",
  "direction_display": "string",
  "type": "string",
  "type_display": "string",
  "sender": 1,
  "sender_name": "string",
  "receiver": 1,
  "receiver_name": "string",
  "created_by": 1,
  "full_name": "string",
  "passport_number": "string",
  "phone_number": "string",
  "license_plate": "string",
  "vehicle_model": "string",
  "start_date": "string",
  "end_date": "string",
  "invoices": [],
  "last_confirmation": {
    "id": 1,
    "expedition": {
      "id": 1,
      "name": "string"
    },
    "confirmed_by": 1,
    "confirmed_by_username": "string",
    "zone": 1,
    "zone_name": "string",
    "status": "string",
    "status_display": "string",
    "confirmed_at": "string"
  }
}
```

## Товары

### Получение списка ТМЦ

**Endpoint:** `GET /goods/`

**Описание:** Получение списка всех товарно-материальных ценностей.

**Ответ (200):**
```json
[
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "unit_of_measurement": "шт",
    "unit_of_measurement_display": "string"
  }
]
```

### Получение данных ТМЦ

**Endpoint:** `GET /goods/{id}/`

**Описание:** Получение данных конкретной ТМЦ.

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "description": "string",
  "unit_of_measurement": "шт",
  "unit_of_measurement_display": "string"
}
```

### Создание новой ТМЦ

**Endpoint:** `POST /goods/`

**Описание:** Создание новой ТМЦ.

**Тело запроса:**
```json
{
  "name": "string",
  "description": "string",
  "unit_of_measurement": "шт"
}
```

**Ответ (201):**
```json
{
  "id": 1,
  "name": "string",
  "description": "string",
  "unit_of_measurement": "шт",
  "unit_of_measurement_display": "string"
}
```

### Обновление данных ТМЦ

**Endpoint:** `PUT /goods/{id}/`

**Описание:** Полное обновление данных ТМЦ.

**Тело запроса:**
```json
{
  "name": "string",
  "description": "string",
  "unit_of_measurement": "шт"
}
```

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "description": "string",
  "unit_of_measurement": "шт",
  "unit_of_measurement_display": "string"
}
```

### Частичное обновление данных ТМЦ

**Endpoint:** `PATCH /goods/{id}/`

**Описание:** Частичное обновление данных ТМЦ.

**Тело запроса:**
```json
{
  "name": "string"
}
```

**Ответ (200):**
```json
{
  "id": 1,
  "name": "string",
  "description": "string",
  "unit_of_measurement": "шт",
  "unit_of_measurement_display": "string"
}
```

### Удаление ТМЦ

**Endpoint:** `DELETE /goods/{id}/`

**Описание:** Удаление ТМЦ.

**Ответ (204):** Нет содержимого

## Подтверждения

### Создание подтверждения

**Endpoint:** `POST /confirm`

**Описание:** Подтверждение экспедиции оператором КПП.

**Тело запроса:**
```json
{
  "expedition_id": 1,
  "zone_id": 1,
  "checkpoint_id": 1,
  "status": "confirmed"
}
```

**Ответ (201):**
```json
{
  "id": 1,
  "expedition": {
    "id": 1,
    "name": "string"
  },
  "confirmed_by": 1,
  "confirmed_by_username": "string",
  "zone": 1,
  "zone_name": "string",
  "status": "string",
  "status_display": "string",
  "confirmed_at": "string"
}
```

### Получение списка подтверждений для зоны

**Endpoint:** `GET /confirmed/zone/{zone_id}`

**Описание:** Получение списка подтверждений для конкретной зоны.

**Ответ (200):**
```json
[
  {
    "id": 1,
    "expedition": {
      "id": 1,
      "name": "string"
    },
    "confirmed_by": 1,
    "confirmed_by_username": "string",
    "zone": 1,
    "zone_name": "string",
    "status": "string",
    "status_display": "string",
    "confirmed_at": "string"
  }
]
```

### Получение списка подтверждений для КПП

**Endpoint:** `GET /confirmed/checkpoint/{checkpoint_id}`

**Описание:** Получение списка подтверждений для конкретного КПП.

**Ответ (200):**
```json
[
  {
    "id": 1,
    "expedition": {
      "id": 1,
      "name": "string"
    },
    "confirmed_by": 1,
    "confirmed_by_username": "string",
    "zone": 1,
    "zone_name": "string",
    "status": "string",
    "status_display": "string",
    "confirmed_at": "string"
  }
]
``` 
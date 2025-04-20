# Краткий обзор API Системы контроля КПП

В этом документе представлен краткий обзор доступных API эндпоинтов системы контроля КПП.

## Аутентификация и пользователи

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/auth/jwt/create/` | Получение JWT токена |
| POST | `/auth/jwt/refresh/` | Обновление JWT токена |
| POST | `/auth/jwt/verify/` | Проверка JWT токена |
| GET | `/auth/details` | Получение данных текущего пользователя |
| POST | `/auth/signup` | Регистрация нового пользователя |
| POST | `/auth/setpass/{token}` | Установка пароля при первом входе |
| GET | `/auth/users` | Получение списка пользователей |
| GET | `/auth/stats` | Получение статистики по пользователям (для администраторов) |

## Организации

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/orgs/` | Получение списка организаций |
| GET | `/orgs/{id}/` | Получение данных организации |
| POST | `/orgs/` | Создание новой организации |
| PUT | `/orgs/{id}/` | Обновление данных организации |
| PATCH | `/orgs/{id}/` | Частичное обновление данных организации |
| DELETE | `/orgs/{id}/` | Удаление организации |

## КПП

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/checkpoints/` | Получение списка КПП |
| GET | `/checkpoints/{id}/` | Получение данных КПП |
| POST | `/checkpoints/` | Создание нового КПП |
| PUT | `/checkpoints/{id}/` | Обновление данных КПП |
| PATCH | `/checkpoints/{id}/` | Частичное обновление данных КПП |
| DELETE | `/checkpoints/{id}/` | Удаление КПП |

## Экспедиции

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/expedition` | Создание новой экспедиции |
| GET | `/expedition/{id}` | Получение данных экспедиции |
| GET | `/expeditions` | Получение списка всех экспедиций |
| GET | `/expeditions/{checkpoint_id}` | Получение списка экспедиций для КПП |
| GET | `/expeditions/brief/{checkpoint_id}` | Получение списка ID экспедиций для КПП |
| GET | `/expedition/status/{expedition_id}` | Получение статуса экспедиции |
| GET | `/expeditions/status` | Получение статусов всех экспедиций |
| GET | `/expeditions/status/{checkpoint_id}` | Получение статусов экспедиций для КПП |

## Товары (ТМЦ)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/goods/` | Получение списка ТМЦ |
| GET | `/goods/{id}/` | Получение данных ТМЦ |
| POST | `/goods/` | Создание новой ТМЦ |
| PUT | `/goods/{id}/` | Обновление данных ТМЦ |
| PATCH | `/goods/{id}/` | Частичное обновление данных ТМЦ |
| DELETE | `/goods/{id}/` | Удаление ТМЦ |

## Подтверждения

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/confirm` | Подтверждение экспедиции |
| GET | `/confirmed/zone/{zone_id}` | Получение списка подтверждений для зоны |
| GET | `/confirmed/checkpoint/{checkpoint_id}` | Получение списка подтверждений для КПП |

## Модели данных

### Пользователь (User)
- `id`: int - Идентификатор
- `username`: string - Имя пользователя
- `role`: string - Роль (logistician, operator, admin)
- `checkpoint`: object - Привязанный КПП (для операторов)
- `is_password_set`: boolean - Установлен ли пароль

### Организация (Organization)
- `id`: int - Идентификатор
- `name`: string - Название
- `address`: string - Адрес
- `phone`: string - Телефон
- `contact_person`: string - Контактное лицо

### КПП (Checkpoint)
- `id`: int - Идентификатор
- `name`: string - Название
- `zone_id`: int - Идентификатор зоны (1 - КПП охраны, 2 - Бюро пропусков, 3 - Склад)
- `zone_name`: string - Название зоны

### Экспедиция (Expedition)
- `id`: int - Идентификатор
- `name`: string - Наименование
- `direction`: string - Направление (IN - въезд, OUT - выезд)
- `type`: string - Тип (auto, selfauto, selfout)
- `sender`: int - Отправитель (ID организации)
- `receiver`: int - Получатель (ID организации)
- `full_name`: string - ФИО водителя/представителя
- `passport_number`: string - Номер паспорта
- `phone_number`: string - Номер телефона
- `license_plate`: string - Гос. номер ТС
- `vehicle_model`: string - Модель ТС
- `start_date`: string - Дата начала
- `end_date`: string - Дата завершения
- `created_by`: int - Создатель (ID пользователя)

### Накладная (Invoice)
- `id`: int - Идентификатор
- `expedition`: int - Экспедиция (ID)
- `number`: string - Номер
- `cargo_description`: string - Описание груза

### ТМЦ (Good)
- `id`: int - Идентификатор
- `name`: string - Название
- `description`: string - Описание
- `unit_of_measurement`: string - Единица измерения (шт, кг, л, м)

### Подтверждение (Confirmation)
- `id`: int - Идентификатор
- `expedition`: int - Экспедиция (ID)
- `confirmed_by`: int - Подтверждающий оператор (ID пользователя)
- `zone`: int - Зона (ID)
- `status`: string - Статус подтверждения (confirmed, cancelled)
- `confirmed_at`: string - Дата и время подтверждения 
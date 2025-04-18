# Инструкция по генерации тестовых данных

В проекте имеется скрипт `generate_test_data.py`, который позволяет быстро заполнить базу данных тестовыми данными для разработки и тестирования.

## Что делает скрипт

1. Выполняет миграции базы данных
2. Создает суперпользователя (admin / admin123)
3. Создает тестовые данные:
   - Зоны КПП (КПП охраны, Бюро пропусков, Склад)
   - Контрольно-пропускные пункты (КПП) для каждой зоны
   - Пользователей (логистов и операторов)
   - Организаций
   - Товары (ТМЦ)
   - Экспедиции с накладными и товарами
   - Подтверждения экспедиций операторами

## Как использовать

Для использования скрипта:

1. **Удалите текущую БД** (если вы хотите полностью очистить данные):
   ```
   rm db.sqlite3
   ```

2. **Запустите скрипт**:
   ```
   python generate_test_data.py
   ```

3. **Дождитесь завершения процесса** - скрипт выведет информацию о созданных объектах.

## Учетные данные для входа

После выполнения скрипта, в системе будут доступны следующие учетные записи:

- **Администратор**: 
  - Логин: admin
  - Пароль: admin123

- **Логисты**:
  - Логин: logist1, logist2
  - Пароль: password123

- **Операторы**:
  - Логин: operator1, operator2, operator3, operator4, operator5, operator6
  - Пароль: password123

## Структура созданных данных

1. **Зоны**:
   - КПП охраны
   - Бюро пропусков
   - Склад

2. **КПП**:
   - КПП №1, КПП №2 (зона КПП охраны)
   - Бюро пропусков №1, Бюро пропусков №2 (зона Бюро пропусков)
   - Склад №1, Склад №2 (зона Склад)

3. **Операторы** - привязаны к соответствующим КПП

4. **Организации** - 5 тестовых организаций

5. **Товары** - 10 наименований строительных товаров

6. **Экспедиции** - 20 экспедиций различных типов (въезд/выезд)

7. **Накладные** - каждая экспедиция имеет от 1 до 3 накладных

8. **Подтверждения** - для половины экспедиций созданы подтверждения в различных зонах

## Примечание

Скрипт проверяет существование объектов перед их созданием, поэтому его можно запускать несколько раз - он не будет создавать дубликаты.

Если вы хотите сгенерировать данные заново, рекомендуется удалить файл базы данных перед запуском скрипта. 
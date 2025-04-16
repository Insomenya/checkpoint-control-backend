import os
import sys
import django
import random
from datetime import date, datetime, timedelta

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkpoint_control.settings')
django.setup()

# Импортируем модели после инициализации Django
from django.contrib.auth import get_user_model
from organizations.models import Organization
from checkpoints.models import Zone, Checkpoint
from expeditions.models import Good, Expedition, Invoice, InvoiceGood
from confirmations.models import Confirmation
from django.core.management import call_command

User = get_user_model()

def run_migrations():
    """Выполнение миграций базы данных"""
    print("Выполнение миграций...")
    call_command('migrate')
    print("Миграции успешно выполнены.")


def create_superuser():
    """Создание суперпользователя"""
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


def create_zones():
    """Создание зон КПП"""
    zones = [
        {'name': 'КПП охраны'},
        {'name': 'Бюро пропусков'},
        {'name': 'Склад'}
    ]
    
    created_zones = []
    for zone_data in zones:
        zone, created = Zone.objects.get_or_create(name=zone_data['name'])
        created_zones.append(zone)
        if created:
            print(f"Создана зона: {zone.name}")
        else:
            print(f"Зона {zone.name} уже существует")
    
    return created_zones


def create_checkpoints(zones):
    """Создание контрольно-пропускных пунктов"""
    checkpoints = [
        {'name': 'КПП №1', 'zone': zones[0]},
        {'name': 'КПП №2', 'zone': zones[0]},
        {'name': 'Бюро пропусков №1', 'zone': zones[1]},
        {'name': 'Бюро пропусков №2', 'zone': zones[1]},
        {'name': 'Склад №1', 'zone': zones[2]},
        {'name': 'Склад №2', 'zone': zones[2]}
    ]
    
    created_checkpoints = []
    for checkpoint_data in checkpoints:
        checkpoint, created = Checkpoint.objects.get_or_create(
            name=checkpoint_data['name'],
            zone=checkpoint_data['zone']
        )
        created_checkpoints.append(checkpoint)
        if created:
            print(f"Создан КПП: {checkpoint.name} (зона: {checkpoint.zone.name})")
        else:
            print(f"КПП {checkpoint.name} уже существует")
    
    return created_checkpoints


def create_users(checkpoints):
    """Создание тестовых пользователей (операторов и логистов)"""
    # Создаем операторов
    operators = [
        {'username': 'operator1', 'role': 'operator', 'checkpoint': checkpoints[0]},
        {'username': 'operator2', 'role': 'operator', 'checkpoint': checkpoints[1]},
        {'username': 'operator3', 'role': 'operator', 'checkpoint': checkpoints[2]},
        {'username': 'operator4', 'role': 'operator', 'checkpoint': checkpoints[3]},
        {'username': 'operator5', 'role': 'operator', 'checkpoint': checkpoints[4]},
        {'username': 'operator6', 'role': 'operator', 'checkpoint': checkpoints[5]}
    ]
    
    # Создаем логистов
    logisticians = [
        {'username': 'logist1', 'role': 'logistician'},
        {'username': 'logist2', 'role': 'logistician'}
    ]
    
    created_users = []
    
    # Создаем операторов
    for operator_data in operators:
        user, created = User.objects.get_or_create(
            username=operator_data['username'],
            defaults={
                'role': operator_data['role'],
                'checkpoint': operator_data['checkpoint'],
                'is_password_set': True
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            print(f"Создан оператор: {user.username} (КПП: {user.checkpoint.name})")
        else:
            print(f"Оператор {user.username} уже существует")
        
        created_users.append(user)
    
    # Создаем логистов
    for logist_data in logisticians:
        user, created = User.objects.get_or_create(
            username=logist_data['username'],
            defaults={
                'role': logist_data['role'],
                'is_password_set': True
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            print(f"Создан логист: {user.username}")
        else:
            print(f"Логист {user.username} уже существует")
        
        created_users.append(user)
    
    return created_users


def create_organizations():
    """Создание тестовых организаций"""
    organizations = [
        {'name': 'ООО "Ромашка"', 'address': 'г. Москва, ул. Ленина, д. 1', 'contact_phone': '+7(495)123-45-67'},
        {'name': 'ЗАО "Орион"', 'address': 'г. Санкт-Петербург, пр. Невский, д. 78', 'contact_phone': '+7(812)765-43-21'},
        {'name': 'ИП Иванов', 'address': 'г. Казань, ул. Баумана, д. 15', 'contact_phone': '+7(843)222-33-44'},
        {'name': 'АО "ТехноСтрой"', 'address': 'г. Новосибирск, ул. Красный проспект, д. 25', 'contact_phone': '+7(383)555-66-77'},
        {'name': 'ООО "ТрансЛогистик"', 'address': 'г. Екатеринбург, ул. Малышева, д. 42', 'contact_phone': '+7(343)888-99-00'}
    ]
    
    created_orgs = []
    for org_data in organizations:
        org, created = Organization.objects.get_or_create(
            name=org_data['name'],
            defaults={
                'address': org_data['address'],
                'contact_phone': org_data['contact_phone']
            }
        )
        created_orgs.append(org)
        if created:
            print(f"Создана организация: {org.name}")
        else:
            print(f"Организация {org.name} уже существует")
    
    return created_orgs


def create_goods():
    """Создание тестовых товаров"""
    goods_data = [
        {'name': 'Кирпич строительный', 'description': 'Красный керамический', 'unit_of_measurement': 'шт'},
        {'name': 'Цемент М500', 'description': 'Портландцемент', 'unit_of_measurement': 'кг'},
        {'name': 'Песок строительный', 'description': 'Речной мытый', 'unit_of_measurement': 'кг'},
        {'name': 'Арматура 12мм', 'description': 'Строительная арматура', 'unit_of_measurement': 'м'},
        {'name': 'Труба ПВХ', 'description': 'Водопроводная', 'unit_of_measurement': 'м'},
        {'name': 'Краска фасадная', 'description': 'Атмосферостойкая', 'unit_of_measurement': 'л'},
        {'name': 'Гвозди строительные', 'description': '120мм', 'unit_of_measurement': 'кг'},
        {'name': 'Доска обрезная', 'description': 'Сосна', 'unit_of_measurement': 'м'},
        {'name': 'Кабель электрический', 'description': 'ВВГ 3x2.5', 'unit_of_measurement': 'м'},
        {'name': 'Плитка керамическая', 'description': 'Напольная', 'unit_of_measurement': 'шт'}
    ]
    
    created_goods = []
    for good_data in goods_data:
        good, created = Good.objects.get_or_create(
            name=good_data['name'],
            defaults={
                'description': good_data['description'],
                'unit_of_measurement': good_data['unit_of_measurement']
            }
        )
        created_goods.append(good)
        if created:
            print(f"Создан товар: {good.name}")
        else:
            print(f"Товар {good.name} уже существует")
    
    return created_goods


def create_expeditions(organizations, users, goods):
    """Создание тестовых экспедиций с накладными и товарами"""
    # Получаем логистов
    logisticians = [user for user in users if user.role == 'logistician']
    
    # Создаем 20 экспедиций
    created_expeditions = []
    
    for i in range(1, 21):
        # Выбираем случайные организации для отправителя и получателя
        sender = random.choice(organizations)
        receiver = random.choice([org for org in organizations if org != sender])
        
        # Выбираем случайного логиста
        created_by = random.choice(logisticians)
        
        # Определяем направление и тип
        direction = random.choice(['IN', 'OUT'])
        exp_type = random.choice(['auto', 'selfauto', 'selfout'])
        
        # Генерируем данные для водителя и транспорта
        full_name = f"Водитель {i}"
        passport_number = f"45{i:02d} {500000 + i:06d}"
        phone_number = f"+7(9{i%10}0){i:02d}-{i*5:02d}-{i*7:02d}"
        license_plate = f"А{100+i} АА 77"
        vehicle_model = random.choice(["ГАЗель", "КАМАЗ", "МАЗ", "Ford Transit", "Volvo", "MAN"])
        
        # Дата начала - от 30 дней назад до сегодня
        days_ago = random.randint(0, 30)
        start_date = date.today() - timedelta(days=days_ago)
        
        # Создаем экспедицию
        expedition = Expedition.objects.create(
            name=f"Экспедиция №{i}",
            direction=direction,
            type=exp_type,
            sender=sender,
            receiver=receiver,
            created_by=created_by,
            full_name=full_name,
            passport_number=passport_number,
            phone_number=phone_number,
            license_plate=license_plate,
            vehicle_model=vehicle_model,
            start_date=start_date
        )
        
        created_expeditions.append(expedition)
        print(f"Создана экспедиция: {expedition.name} ({expedition.get_direction_display()}, {expedition.get_type_display()})")
        
        # Создаем от 1 до 3 накладных для каждой экспедиции
        num_invoices = random.randint(1, 3)
        for j in range(1, num_invoices + 1):
            invoice = Invoice.objects.create(
                expedition=expedition,
                number=f"ТТН-{i}-{j}",
                cargo_description=f"Описание груза для накладной ТТН-{i}-{j}"
            )
            
            # Создаем от 1 до 5 позиций товаров для каждой накладной
            num_goods = random.randint(1, 5)
            selected_goods = random.sample(goods, num_goods)
            
            for good in selected_goods:
                quantity = random.randint(1, 100) if good.unit_of_measurement in ['шт', 'кг'] else random.randint(1, 20)
                
                InvoiceGood.objects.create(
                    invoice=invoice,
                    good=good,
                    quantity=quantity
                )
            
            print(f"  Создана накладная: {invoice.number} с {num_goods} товарами")
    
    return created_expeditions


def create_confirmations(expeditions, users, zones):
    """Создание тестовых подтверждений для экспедиций"""
    # Получаем операторов
    operators = [user for user in users if user.role == 'operator']
    
    created_confirmations = []
    
    # Для половины экспедиций создаем подтверждения
    for expedition in expeditions[:len(expeditions)//2]:
        # Определяем последовательность зон в зависимости от направления
        if expedition.direction == 'IN':
            zone_sequence = zones[:3]  # КПП охраны -> Бюро пропусков -> Склад
        else:
            zone_sequence = zones[2::-1]  # Склад -> Бюро пропусков -> КПП охраны
        
        # Создаем от 1 до 3 подтверждений для экспедиции (в зависимости от прогресса)
        num_confirmations = random.randint(1, len(zone_sequence))
        
        # Смещение времени для подтверждений
        time_offset = 0
        
        for i in range(num_confirmations):
            zone = zone_sequence[i]
            
            # Выбираем оператора из соответствующей зоны
            zone_operators = [op for op in operators if op.checkpoint.zone == zone]
            if not zone_operators:
                continue
            
            confirmed_by = random.choice(zone_operators)
            status = random.choices(['confirmed', 'cancelled'], weights=[0.9, 0.1])[0]
            
            # Создаем дату подтверждения
            confirmed_at = datetime.now() - timedelta(days=random.randint(0, 20), hours=time_offset)
            time_offset += random.randint(1, 12)  # Добавляем от 1 до 12 часов для следующего подтверждения
            
            confirmation = Confirmation.objects.create(
                expedition=expedition,
                confirmed_by=confirmed_by,
                zone=zone,
                status=status,
                confirmed_at=confirmed_at
            )
            
            created_confirmations.append(confirmation)
            print(f"Создано подтверждение: {confirmation} ({confirmation.get_status_display()})")
            
            # Если статус отмены, прекращаем цепочку подтверждений
            if status == 'cancelled':
                break
        
        # Если экспедиция завершена, устанавливаем end_date
        if num_confirmations == len(zone_sequence) and zone_sequence[-1] == zones[0]:  # КПП охраны
            if expedition.direction == 'OUT':
                expedition.end_date = date.today() - timedelta(days=random.randint(0, 10))
                expedition.save()
                print(f"Экспедиция {expedition.name} завершена {expedition.end_date}")
    
    return created_confirmations


def generate_test_data():
    """Основная функция для генерации тестовых данных"""
    run_migrations()
    create_superuser()
    
    zones = create_zones()
    checkpoints = create_checkpoints(zones)
    users = create_users(checkpoints)
    organizations = create_organizations()
    goods = create_goods()
    expeditions = create_expeditions(organizations, users, goods)
    confirmations = create_confirmations(expeditions, users, zones)
    
    print("\nГенерация тестовых данных завершена!")
    print(f"Создано:")
    print(f"- {len(zones)} зон")
    print(f"- {len(checkpoints)} КПП")
    print(f"- {len(users)} пользователей")
    print(f"- {len(organizations)} организаций")
    print(f"- {len(goods)} товаров")
    print(f"- {len(expeditions)} экспедиций")
    print(f"- {len(confirmations)} подтверждений")
    
    print("\nУчетные данные для доступа:")
    print("Администратор: admin / admin123")
    print("Логисты: logist1, logist2 / password123")
    print("Операторы: operator1-operator6 / password123")


if __name__ == "__main__":
    generate_test_data() 
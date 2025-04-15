from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from organizations.models import Organization

User = get_user_model()

class Good(models.Model):
    UNITS = (
        ('шт', 'Штуки'),
        ('кг', 'Килограммы'),
        ('л', 'Литры'),
        ('м', 'Метры')
    )
    
    name = models.CharField(_("Название"), max_length=255, null=False, blank=False)
    description = models.TextField(_("Описание"), null=True, blank=True)
    unit_of_measurement = models.CharField(_("Единица измерения"), max_length=50, choices=UNITS, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = _('ТМЦ')
        verbose_name_plural = _('ТМЦ')

class Expedition(models.Model):
    DIRECTIONS = (
        ('IN', 'Въезд'),
        ('OUT', 'Выезд')
    )
    
    TYPES = (
        ('auto', 'Авто'),
        ('selfauto', 'Самовывоз'),
        ('selfout', 'Самовынос')
    )
    
    name = models.CharField(_("Наименование"), max_length=255, null=False, blank=False)
    direction = models.CharField(_("Направление"), max_length=255, choices=DIRECTIONS, null=False, blank=False)
    type = models.CharField(_("Тип"), max_length=255, choices=TYPES, null=False, blank=False)
    sender = models.ForeignKey(Organization, verbose_name=_("Отправитель"), on_delete=models.CASCADE, related_name="sent_expeditions")
    receiver = models.ForeignKey(Organization, verbose_name=_("Получатель"), on_delete=models.CASCADE, related_name="received_expeditions")
    created_by = models.ForeignKey(User, verbose_name=_("Создал"), on_delete=models.CASCADE, related_name="created_expeditions")
    full_name = models.CharField(_("ФИО"), max_length=255, null=True, blank=True)
    passport_number = models.CharField(_("Номер паспорта"), max_length=50, null=True, blank=True)
    phone_number = models.CharField(_("Номер телефона"), max_length=20, null=True, blank=True)
    license_plate = models.CharField(_("Гос. номер ТС"), max_length=20, null=True, blank=True)
    vehicle_model = models.CharField(_("Модель ТС"), max_length=255, null=True, blank=True)
    start_date = models.DateField(_("Дата начала"), null=True, blank=True)
    end_date = models.DateField(_("Дата завершения"), null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_direction_display()}, {self.get_type_display()})"
    
    class Meta:
        verbose_name = _('экспедиция')
        verbose_name_plural = _('экспедиции')

class Invoice(models.Model):
    expedition = models.ForeignKey(Expedition, verbose_name=_("Экспедиция"), on_delete=models.CASCADE, related_name="invoices")
    number = models.CharField(_("Номер"), max_length=255, null=False, blank=False)
    cargo_description = models.TextField(_("Описание груза"), null=True, blank=True)
    
    def __str__(self):
        return f"Накладная {self.number}"
    
    class Meta:
        verbose_name = _('накладная')
        verbose_name_plural = _('накладные')

class InvoiceGood(models.Model):
    invoice = models.ForeignKey(Invoice, verbose_name=_("Накладная"), on_delete=models.CASCADE, related_name="invoice_goods")
    good = models.ForeignKey(Good, verbose_name=_("ТМЦ"), on_delete=models.CASCADE, related_name="invoice_goods")
    quantity = models.FloatField(_("Количество"), null=False, blank=False)
    
    def __str__(self):
        return f"{self.good.name} ({self.quantity} {self.good.unit_of_measurement}) в {self.invoice.number}"
    
    class Meta:
        verbose_name = _('ТМЦ в накладной')
        verbose_name_plural = _('ТМЦ в накладных')
        unique_together = ('invoice', 'good')

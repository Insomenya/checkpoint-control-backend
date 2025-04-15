from django.db import models
from django.utils.translation import gettext_lazy as _

class Organization(models.Model):
    name = models.CharField(_("Название"), max_length=255, null=False, blank=False)
    address = models.CharField(_("Адрес"), max_length=255, null=True, blank=True)
    contact_phone = models.CharField(_("Контактный телефон"), max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = _('организация')
        verbose_name_plural = _('организации')

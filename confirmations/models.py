from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from expeditions.models import Expedition
from checkpoints.models import Zone

User = get_user_model()

class Confirmation(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отклонено')
    )
    
    expedition = models.ForeignKey(Expedition, verbose_name=_("Экспедиция"), on_delete=models.CASCADE, related_name="confirmations")
    confirmed_by = models.ForeignKey(User, verbose_name=_("Подтверждено"), on_delete=models.CASCADE, related_name="confirmations")
    zone = models.ForeignKey(Zone, verbose_name=_("Зона"), on_delete=models.CASCADE, related_name="confirmations")
    status = models.CharField(_("Статус"), max_length=50, choices=STATUS_CHOICES, null=False, blank=False)
    confirmed_at = models.DateTimeField(_("Дата и время подтверждения"), auto_now_add=True)
    
    def __str__(self):
        return f"Подтверждение {self.expedition.name} в зоне {self.zone.name} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = _('подтверждение')
        verbose_name_plural = _('подтверждения')
        ordering = ['-confirmed_at']

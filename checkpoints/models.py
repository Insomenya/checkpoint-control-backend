from django.db import models
from django.utils.translation import gettext_lazy as _

class Zone(models.Model):
    name = models.CharField(_("Название"), max_length=255, null=False, blank=False)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = _('зона')
        verbose_name_plural = _('зоны')

class Checkpoint(models.Model):
    name = models.CharField(_("Название"), max_length=255, null=False, blank=False)
    zone = models.ForeignKey(Zone, verbose_name=_("Зона"), on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.zone.name})"
    
    class Meta:
        verbose_name = _('КПП')
        verbose_name_plural = _('КПП')

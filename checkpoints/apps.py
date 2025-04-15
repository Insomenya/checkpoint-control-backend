from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CheckpointsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkpoints'
    verbose_name = _('КПП и зоны')

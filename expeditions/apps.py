from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExpeditionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expeditions'
    verbose_name = _('Экспедиции и ТМЦ')

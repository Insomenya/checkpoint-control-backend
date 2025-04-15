from django.contrib import admin
from .models import Zone, Checkpoint

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone')
    list_filter = ('zone',)
    search_fields = ('name',)

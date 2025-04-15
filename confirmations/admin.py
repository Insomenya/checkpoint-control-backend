from django.contrib import admin
from .models import Confirmation

@admin.register(Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = ('expedition', 'confirmed_by', 'zone', 'status', 'confirmed_at')
    list_filter = ('status', 'zone', 'confirmed_at')
    search_fields = ('expedition__name', 'confirmed_by__username')

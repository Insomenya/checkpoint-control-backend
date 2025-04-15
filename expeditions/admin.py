from django.contrib import admin
from .models import Good, Expedition, Invoice, InvoiceGood

@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measurement')
    list_filter = ('unit_of_measurement',)
    search_fields = ('name', 'description')

class InvoiceGoodInline(admin.TabularInline):
    model = InvoiceGood
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'expedition', 'cargo_description')
    list_filter = ('expedition',)
    search_fields = ('number', 'cargo_description')
    inlines = [InvoiceGoodInline]

class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 1

@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'type', 'sender', 'receiver', 'start_date', 'end_date')
    list_filter = ('direction', 'type', 'start_date', 'end_date')
    search_fields = ('name', 'full_name', 'passport_number', 'phone_number', 'license_plate')
    inlines = [InvoiceInline]

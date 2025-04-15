from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'is_password_set', 'checkpoint')
    list_filter = ('role', 'is_password_set')
    search_fields = ('username',)
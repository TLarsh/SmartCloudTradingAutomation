from django.contrib import admin
from .models import User, BrokerAccount, Signal

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_staff', 'date_joined')

@admin.register(BrokerAccount)
class BrokerAccountAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'provider', 'user', 'is_demo', 'created_at')

@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ('webhook_id', 'user', 'processed', 'created_at')

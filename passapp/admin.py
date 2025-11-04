from django.contrib import admin
from .models import Password, Service, Account

class PasswordAdmin(admin.ModelAdmin):
    list_display = ['code', 'passwd', 'description']
    ordering = ('code',)
    search_fields = ('code', 'description')
    list_filter = ['code']

admin.site.register(Password, PasswordAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'description']
    ordering = ('name',)
    search_fields = ('name', 'url', 'description')
    list_filter = ['name']

admin.site.register(Service, ServiceAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ['service', 'who', 'login','access', 'description']
    ordering = ('service',)
    search_fields = ('service', 'who', 'login','access', 'description')
    list_filter = ['who', 'service']

admin.site.register(Account, AccountAdmin)
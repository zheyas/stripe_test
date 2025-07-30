from django.contrib import admin

from .models import Tax


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'get_currency', 'description')

    def get_currency(self, obj):
        return obj.get_currency_display()
    get_currency.short_description = 'Валюта'

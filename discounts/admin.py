from django.contrib import admin
from .models import Discount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'get_currency', 'stripe_coupon_id')

    def get_currency(self, obj):
        return obj.get_currency_display()
    get_currency.short_description = 'Валюта'

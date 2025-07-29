# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    verbose_name = "Товар"
    verbose_name_plural = "Товары в заказе"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'display_items', 'total_amount_display')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]
    exclude = ('items',)  # исключаем поле ManyToMany, чтобы не дублировать с inline

    def display_items(self, obj):
        return ", ".join([f"{oi.item.name} (x{oi.quantity})" for oi in obj.orderitem_set.all()])
    display_items.short_description = 'Товары'

    def total_amount_display(self, obj):
        if obj.orderitem_set.exists():
            currency = obj.orderitem_set.first().item.currency.upper()
            return f"{obj.total_amount / 100:.2f} {currency}"
        return f"{obj.total_amount / 100:.2f}"
    total_amount_display.short_description = 'Итого'

from django.db import models

from discounts.models import Discount
from items.models import Item
from taxes.models import Tax


class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem')
    discount = models.ForeignKey(Discount, null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL
                                 )
    tax = models.ForeignKey(Tax, null=True, blank=True,
                            on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount_cents(self):
        total = 0
        for order_item in self.orderitem_set.all():
            price = order_item.item.get_discounted_price(
            ) or order_item.item.price
            total += int(price * 100) * order_item.quantity

        if self.discount:
            total -= int(total * self.discount.percentage / 100)

        if self.tax:
            total += int(total * self.tax.rate)

        return max(total, 0)

    @property
    def total_amount(self):
        return (self.total_amount_cents() / 100)

    def __str__(self):
        return f"Order #{self.id} ({self.items.count()} items)"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # количество товара

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"

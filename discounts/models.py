
from django.db import models

from items.models import Item


class Discount(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Скидка в %, например 10.00",
        default=0
    )
    items = models.ManyToManyField(
        Item, related_name="discounts"
    )
    stripe_coupon_id = models.CharField(
        max_length=255, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

    def get_currency_display(self):
        currencies = self.items.values_list('currency', flat=True).distinct()
        if currencies.count() == 1:
            return currencies.first().upper()
        return "несколько валют"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'percentage'],
                                    name='unique_discount_name_percentage')
        ]

from decimal import Decimal, ROUND_HALF_UP
from django.db import models

CURRENCY_CHOICES = (
    ('usd', 'USD ($)'),
    ('eur', 'EUR (€)'),
    ('rub', 'RUB (₽)'),
)


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default='rub'
    )

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        discount = self.discounts.first()
        if discount:
            return (self.price * (
                    1 - discount.percentage / 100)
                    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return self.price

    def get_tax_amount(self, base_price=None):
        if base_price is None:
            base_price = self.get_discounted_price()
        total_percentage = sum(tax.percentage for tax in self.taxes.all())
        return (base_price * total_percentage / 100).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def get_final_price(self):
        discounted_price = self.get_discounted_price()
        tax_amount = self.get_tax_amount(discounted_price)
        return (discounted_price + tax_amount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

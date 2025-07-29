#taxes/models.py
from django.db import models
from items.models import Item

class Tax(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название налога")
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Процент налога, например 10.00",
        default=0,
        verbose_name="Процент налога"
    )
    items = models.ManyToManyField(Item, related_name="taxes", verbose_name="Выберите товары")
    description = models.TextField(blank=True, null=True, verbose_name="Описание налога")

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

    def get_currency_display(self):
        currencies = self.items.values_list('currency', flat=True).distinct()
        if currencies.count() == 1:
            return currencies.first().upper()
        return "несколько валют"

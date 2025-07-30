from django import forms
from .models import Discount


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'percentage', 'items']
        widgets = {
            'items': forms.CheckboxSelectMultiple(
                attrs={'class': 'styled-checkbox'}
            ),
        }
        labels = {
            'name': 'Название акции',
            'percentage': 'Скидка (%)',
            'items': 'Выберите товары',
        }

    def clean(self):
        cleaned_data = super().clean()
        items = cleaned_data.get('items')
        if not items:
            raise forms.ValidationError(
                "Выберите хотя бы один товар для применения скидки."
            )
        return cleaned_data

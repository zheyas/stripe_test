from django import forms
from .models import Tax

class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['name', 'percentage', 'description', 'items']
        widgets = {
            'items': forms.CheckboxSelectMultiple(attrs={'class': 'styled-checkbox'}),
            'description': forms.Textarea(attrs={'rows': 3, 'style': 'resize:none;'}),
        }
        labels = {
            'name': 'Название налога',
            'percentage': 'Процент налога',
            'description': 'Описание налога',
            'items': 'Выберите товары',
        }

    def clean(self):
        cleaned_data = super().clean()
        items = cleaned_data.get('items')
        if not items:
            raise forms.ValidationError("Выберите хотя бы один товар для применения налога.")
        return cleaned_data

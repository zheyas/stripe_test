# items/forms.py
from django import forms


class BuyForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())

from django import forms


class OrderPayForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput)

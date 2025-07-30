from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from .forms import BuyForm
from .services import create_payment_intent
from django.conf import settings
from django.views.generic import ListView
from .models import Item
from django.core.exceptions import ValidationError


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class ItemDetailView(View):
    def get(self, request, id):
        item = get_object_or_404(Item, id=id)
        form = BuyForm(initial={'item_id': item.id})

        try:
            payment_intent = create_payment_intent(item)
            client_secret = payment_intent.client_secret
            error = None
        except ValidationError as e:
            client_secret = None
            error = str(e)

        context = {
            'item': item,
            'form': form,
            'price': item.price,
            'discounted_price': item.get_discounted_price(),
            'tax_amount': item.get_tax_amount(),
            'final_price': item.get_final_price(),
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': client_secret,
            'error': error,
        }
        return render(request, 'item_detail.html', context)

    def post(self, request, id):
        item = get_object_or_404(Item, id=id)
        form = BuyForm(request.POST)
        context = {
            'item': item,
            'form': form,
            'price': item.price,
            'discounted_price': item.get_discounted_price(),
            'tax_amount': item.get_tax_amount(),
            'final_price': item.get_final_price(),
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': None,
            'error': None,
        }
        return render(request, 'item_detail.html', context)


class ItemListView(ListView):
    model = Item
    template_name = 'items-list.html'
    context_object_name = 'items'

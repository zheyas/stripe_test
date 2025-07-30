from django.http import JsonResponse
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from .models import Order
from decimal import Decimal, ROUND_HALF_UP
from django.views.generic import ListView


stripe.api_key = settings.STRIPE_SECRET_KEY


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.select_related('item').all()

    items_with_totals = []
    subtotal = Decimal('0.00')

    for oi in order_items:
        discounted_price = oi.item.get_discounted_price()
        line_total = (discounted_price * oi.quantity).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        subtotal += line_total
        items_with_totals.append({
            'order_item': oi,
            'discounted_price': discounted_price,
            'line_total': line_total,
            'old_price': oi.item.price,
        })

    # Пример налога 10% (замени на свою логику)
    tax_percentage = Decimal('10.0')
    tax_amount = (subtotal * tax_percentage / 100).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )
    total_amount = subtotal + tax_amount

    context = {
        'order': order,
        'items_with_totals': items_with_totals,
        'subtotal_rub': subtotal,
        'tax_amount_rub': tax_amount,
        'total_amount_rub': total_amount,
        'form': None,  # если есть форма, передай сюда
    }
    return render(request, 'order_detail.html', context)


def buy_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    line_items = []
    for order_item in order.orderitem_set.select_related("item"):
        item = order_item.item
        price = item.get_discounted_price() or item.price
        # Предполагаем, что price уже в центах для Stripe, иначе надо умножать
        line_items.append({
            'price_data': {
                'currency': item.currency.lower(),
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(price * 100),
            },
            'quantity': order_item.quantity,
        })

    discounts = []
    if order.discount and order.discount.stripe_coupon_id:
        discounts.append({
            'coupon': order.discount.stripe_coupon_id,
        })

    tax_rates = []
    if order.tax and order.tax.stripe_tax_rate_id:
        tax_rates.append(order.tax.stripe_tax_rate_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        discounts=discounts if discounts else None,
        tax_rates=tax_rates if tax_rates else None,
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return JsonResponse({'id': session.id})


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'  # путь внутри templates/
    context_object_name = 'orders'            # удобное имя в шаблоне

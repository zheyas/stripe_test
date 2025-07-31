
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Order
from .services import (StripeSessionCreateError, build_stripe_checkout_session,
                       calculate_order_totals)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    (items_with_totals, subtotal, tax_amount,
     total_amount) = calculate_order_totals(order)

    context = {
        'order': order,
        'items_with_totals': items_with_totals,
        'subtotal_rub': subtotal,
        'tax_amount_rub': tax_amount,
        'total_amount_rub': total_amount,
        'form': None,  # если есть форма, передай её тут
    }
    return render(request, 'order_detail.html', context)


def buy_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    try:
        session = build_stripe_checkout_session(order, request)
        return JsonResponse({'id': session.id})
    except StripeSessionCreateError as e:
        return JsonResponse({'error': str(e)}, status=400)


class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

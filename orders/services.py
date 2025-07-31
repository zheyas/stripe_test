from decimal import ROUND_HALF_UP, Decimal

import stripe
from django.conf import settings


class StripeSessionCreateError(Exception):
    def __init__(self, message, code=None):
        self.code = code
        super().__init__(message)


def calculate_order_totals(order):
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

    tax_percentage = Decimal('10.0')
    tax_amount = (subtotal * tax_percentage / 100).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )
    total_amount = subtotal + tax_amount

    return items_with_totals, subtotal, tax_amount, total_amount


def build_stripe_checkout_session(order, request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    line_items = []
    for order_item in order.orderitem_set.select_related("item"):
        item = order_item.item
        price = item.get_discounted_price() or item.price
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
    if (hasattr(order, 'discount') and order.
            discount and order.discount.stripe_coupon_id):
        discounts.append({'coupon': order.discount.stripe_coupon_id})

    tax_rates = []
    if hasattr(order, 'tax') and order.tax and order.tax.stripe_tax_rate_id:
        tax_rates.append(order.tax.stripe_tax_rate_id)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            discounts=discounts if discounts else None,
            tax_rates=tax_rates if tax_rates else None,
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return session
    except stripe.error.StripeError as e:
        raise StripeSessionCreateError(str(e))

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(item):
    final_price = item.get_final_price()
    amount = int(final_price * 100)

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=item.currency,
        description=f"Оплата товара: {item.name}",
        metadata={
            "item_id": str(item.id),
            "item_name": item.name,
        }
    )
    return payment_intent

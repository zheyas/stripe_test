import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_coupon(discount):
    """
    Создаёт купон в Stripe на основе объекта Discount.
    :param discount: объект Discount (не сохранённый)
    :return: id купона Stripe
    """
    stripe_coupon = stripe.Coupon.create(
        name=discount.name,
        percent_off=float(discount.percentage),
        duration="once",
    )
    return stripe_coupon["id"]

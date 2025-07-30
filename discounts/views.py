import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DiscountForm
from django.views.generic import ListView
from .models import Discount

stripe.api_key = settings.STRIPE_SECRET_KEY


class DiscountListView(ListView):
    model = Discount
    template_name = 'discounts/discount_list.html'
    context_object_name = 'discounts'


def create_discount(request):
    if request.method == "POST":
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)

            # Создание купона Stripe
            stripe_coupon = stripe.Coupon.create(
                name=discount.name,
                percent_off=float(discount.percentage),
                duration="once",
            )

            discount.stripe_coupon_id = stripe_coupon["id"]
            discount.save()
            form.save_m2m()  # сохраняем связь с товарами

            return redirect("admin:discounts_discount_changelist")
        selected_items = (request.
                          POST.getlist('items'))
    else:
        form = DiscountForm()
        selected_items = []

    return render(request, "create_discount.html",
                  {"form": form, "selected_items": selected_items})


def discount_detail(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    return render(request, 'discounts/discount_detail.html',
                  {'discount': discount})

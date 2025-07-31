from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .business import create_stripe_coupon
from .forms import DiscountForm
from .models import Discount


class DiscountListView(ListView):
    model = Discount
    template_name = 'discounts/discount_list.html'
    context_object_name = 'discounts'


def create_discount(request):
    if request.method == "POST":
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)

            # Вызов бизнес-логики, а не Stripe напрямую!
            discount.stripe_coupon_id = create_stripe_coupon(discount)
            discount.save()
            form.save_m2m()  # сохраняем связь с товарами

            return redirect("admin:discounts_discount_changelist")
        selected_items = request.POST.getlist('items')
    else:
        form = DiscountForm()
        selected_items = []

    return render(request, "create_discount.html",
                  {"form": form, "selected_items": selected_items})


def discount_detail(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    return render(request, 'discounts/discount_detail.html',
                  {'discount': discount})

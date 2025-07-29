#taxes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tax
from .forms import TaxForm

def tax_list(request):
    taxes = Tax.objects.all()
    return render(request, 'taxes/tax_list.html', {'taxes': taxes})

def tax_create(request):
    if request.method == 'POST':
        form = TaxForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tax_list')
    else:
        form = TaxForm()
    return render(request, 'taxes/tax_form.html', {'form': form, 'title': 'Создать налог'})

def tax_update(request, pk):
    tax = get_object_or_404(Tax, pk=pk)
    if request.method == 'POST':
        form = TaxForm(request.POST, instance=tax)
        if form.is_valid():
            form.save()
            return redirect('tax_list')
    else:
        form = TaxForm(instance=tax)
    return render(request, 'taxes/tax_form.html', {'form': form, 'title': 'Редактировать налог'})

def tax_delete(request, pk):
    tax = get_object_or_404(Tax, pk=pk)
    if request.method == 'POST':
        tax.delete()
        return redirect('tax_list')
    return render(request, 'taxes/tax_confirm_delete.html', {'tax': tax})

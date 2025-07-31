from django.urls import path

from . import views
from .views import DiscountListView

urlpatterns = [
    # Список всех скидок: /discounts/
    path('', DiscountListView.as_view(), name='discounts-list'),
    # Создать скидку: /discounts/create/
    path('create/', views.create_discount, name='create_discount'),
    # Детальная страница скидки: /discounts/<id>/
    path('<int:pk>/', views.discount_detail, name='discount_detail'),
]

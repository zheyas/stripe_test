from django.urls import path

from . import views
from .views import OrderListView

urlpatterns = [
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('buy/order/<int:order_id>/', views.buy_order, name='buy_order'),
    path('orders/', OrderListView.as_view(), name='orders-list'),
]

from django.urls import path

from . import views
from .views import OrderListView

urlpatterns = [
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('buy/<int:order_id>/', views.buy_order, name='buy_order'),
    path('', OrderListView.as_view(), name='orders-list'),
]

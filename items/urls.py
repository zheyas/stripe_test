from django.urls import path

from .views import ItemListView  # 🔹 добавляем список
from .views import CancelView, ItemDetailView, SuccessView

urlpatterns = [
    path('items/', ItemListView.as_view(), name='items-list'),
    path('item/<int:id>/', ItemDetailView.as_view(), name='item-detail'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]

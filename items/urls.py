from django.urls import path
from .views import ItemDetailView, SuccessView, CancelView
from .views import ItemListView  # 🔹 добавляем список

urlpatterns = [
    path('items/', ItemListView.as_view(), name='items-list'),  # ✅ маршрут для списка товаров
    path('item/<int:id>/', ItemDetailView.as_view(), name='item_detail'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]

from django.urls import path

from .views import CancelView, ItemDetailView, ItemListView, SuccessView

urlpatterns = [
    path('', ItemListView.as_view(), name='items-list'),
    path('<int:id>/', ItemDetailView.as_view(), name='item-detail'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]

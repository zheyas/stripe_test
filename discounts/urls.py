from django.urls import path
from . import views
from .views import DiscountListView


urlpatterns = [
    path('discounts/', DiscountListView.as_view(), name='discounts-list'),
    path('create/', views.create_discount, name='create_discount'),
    path('<int:pk>/', views.discount_detail, name='discount_detail'),

]

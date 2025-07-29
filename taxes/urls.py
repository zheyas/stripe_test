#taxes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('taxes/', views.tax_list, name='tax_list'),
    path('taxes/create/', views.tax_create, name='tax_create'),
    path('taxes/edit/<int:pk>/', views.tax_update, name='tax_edit'),
    path('taxes/delete/<int:pk>/', views.tax_delete, name='tax_delete'),
]

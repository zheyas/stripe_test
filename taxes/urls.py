from django.urls import path

from . import views

urlpatterns = [
    path('', views.tax_list, name='tax_list'),
    path('create/', views.tax_create, name='tax_create'),
    path('edit/<int:pk>/', views.tax_update, name='tax_edit'),
    path('delete/<int:pk>/', views.tax_delete, name='tax_delete'),
]

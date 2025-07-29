#stripe_test/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('', include('items.urls')),
    path('', include('orders.urls')),
    path('', include('discounts.urls')),
    path('', include('taxes.urls')),

]
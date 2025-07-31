from django.contrib import admin
from django.urls import include, path

from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('items/', include('items.urls')),
    path('orders/', include('orders.urls')),
    path('discounts/', include('discounts.urls')),
    path('taxes/', include('taxes.urls')),
]

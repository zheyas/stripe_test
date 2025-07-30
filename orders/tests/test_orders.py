# orders/tests/test_views.py
from decimal import Decimal

import pytest
from django.urls import reverse

from orders.models import Item, Order, OrderItem


@pytest.mark.django_db
def test_order_list_view(client):
    order = Order.objects.create()
    url = reverse('orders-list')  # name из urls.py
    response = client.get(url)
    assert response.status_code == 200
    assert f'{order.id}' in response.content.decode()


@pytest.mark.django_db
def test_buy_order_view(client, mocker):
    item = Item.objects.create(name='Товар', price=100, currency='RUB')
    order = Order.objects.create()
    OrderItem.objects.create(order=order, item=item, quantity=1)

    mock_session = mocker.Mock()
    mock_session.id = 'sess_test_123'
    mock_create = mocker.patch(
        'orders.views.stripe.checkout.Session.create',
        return_value=mock_session
    )

    url = reverse('buy_order', args=[order.id])  # убедись, что такой урл есть
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 'sess_test_123'
    assert mock_create.called


@pytest.mark.django_db
def test_order_detail_view(client):
    # Подготовка данных
    item = Item.objects.create(name='Товар', price=Decimal('100.00'),
                               currency='RUB')
    order = Order.objects.create()
    OrderItem.objects.create(order=order, item=item, quantity=2)

    url = reverse('order_detail', args=[order.id])
    response = client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    assert 'Товар' in html
    assert '100.00' in html or '200.00' in html  # сумма за 2 товара

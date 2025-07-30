import pytest
from django.urls import reverse

from items import services
from items.models import Item


@pytest.mark.django_db
def test_item_list_view(client):
    Item.objects.create(name="Тест", price=100, currency='usd')
    url = reverse('items-list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Тест' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_item_detail_view_post(client):
    item = Item.objects.create(name="Тест", price=100, currency='usd')
    url = reverse('item-detail', kwargs={'id': item.id})
    data = {'item_id': item.id}
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'Тест' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_item_detail_view_get(client, mocker):
    # Создаём товар в БД
    item = Item.objects.create(name="Тест", price=100, currency='usd')

    # Мокаем Stripe PaymentIntent
    mock_payment_intent = mocker.Mock()
    mock_payment_intent.client_secret = 'fake-secret'
    patcher = mocker.patch(
        'items.services.stripe.PaymentIntent.create',
        return_value=mock_payment_intent
    )

    url = reverse('item-detail', kwargs={'id': item.id})
    response = client.get(url)

    assert response.status_code == 200
    assert 'fake-secret' in response.content.decode('utf-8')
    patcher.assert_called()   # Stripe PaymentIntent должен быть вызван


class DummyItem:
    id = 123
    name = "Тестовый товар"
    currency = "usd"
    def get_final_price(self): return 9.99


@pytest.mark.django_db
def test_create_payment_intent(mocker):
    dummy_item = DummyItem()
    mock_payment_intent = mocker.Mock()
    mock_payment_intent.client_secret = "fake_secret"

    patcher = mocker.patch('items.services.stripe.PaymentIntent.create',
                           return_value=mock_payment_intent)
    res = services.create_payment_intent(dummy_item)

    assert res.client_secret == "fake_secret"
    patcher.assert_called_once_with(
        amount=999,        # 9.99*100 = 999
        currency="usd",
        description="Оплата товара: Тестовый товар",
        metadata={"item_id": "123", "item_name": "Тестовый товар"}
    )

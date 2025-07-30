import pytest
from django.urls import reverse
from taxes.models import Tax
from items.models import Item


@pytest.mark.django_db
def test_tax_list_view(client):
    Tax.objects.create(name="НДС", percentage=20)
    url = reverse('tax_list')
    response = client.get(url)
    assert response.status_code == 200
    assert "НДС" in response.content.decode()


@pytest.mark.django_db
def test_tax_create_view_get(client):
    url = reverse('tax_create')
    response = client.get(url)
    assert response.status_code == 200
    assert "Создать налог" in response.content.decode()


@pytest.mark.django_db
def test_tax_create_view_post(client):
    item = Item.objects.create(name='Товар', price=100, currency='RUB')
    url = reverse('tax_create')
    data = {
        'name': 'Экспорт',
        'percentage': 0,
        'items': [item.pk]
    }
    response = client.post(url, data)
    # print(response.context['form'].errors)  # Раскомментируй для отладки
    assert response.status_code == 302
    assert Tax.objects.filter(name="Экспорт", percentage=0).exists()


@pytest.mark.django_db
def test_tax_update_view_get(client):
    tax = Tax.objects.create(name="НДС", percentage=20)
    url = reverse('tax_edit', args=[tax.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert "Редактировать налог" in response.content.decode()


@pytest.mark.django_db
def test_tax_update_view_post(client):
    item = Item.objects.create(name='Товар', price=100, currency='RUB')
    tax = Tax.objects.create(name="НДС", percentage=20)
    tax.items.add(item)
    url = reverse('tax_edit', args=[tax.pk])
    data = {
        'name': 'Новый НДС',
        'percentage': 18,
        'items': [item.pk]
    }
    response = client.post(url, data)
    # print(response.context['form'].errors)  # Раскомментируй для отладки
    assert response.status_code == 302
    tax.refresh_from_db()
    assert tax.name == 'Новый НДС'
    assert tax.percentage == 18


@pytest.mark.django_db
def test_tax_delete_view_get(client):
    tax = Tax.objects.create(name="Устаревший", percentage=15)
    url = reverse('tax_delete', args=[tax.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert "Устаревший" in response.content.decode()


@pytest.mark.django_db
def test_tax_delete_view_post(client):
    tax = Tax.objects.create(name="Устаревший", percentage=15)
    url = reverse('tax_delete', args=[tax.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert not Tax.objects.filter(pk=tax.pk).exists()

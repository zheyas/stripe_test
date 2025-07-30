import pytest
from django.urls import reverse
from discounts.models import Discount
from items.models import Item

pytestmark = pytest.mark.django_db


def create_test_items(n=2):
    items = []
    for i in range(n):
        items.append(Item.objects.create(
            name=f"Item {i}",
            price=100 + i,
            currency="rub"
        ))
    return items


def create_discount(name="TestDisc", percentage=10, items=None):
    d = Discount.objects.create(name=name, percentage=percentage)
    if items:
        d.items.set(items)
    return d


def test_discount_list_view(client):
    d1 = create_discount("disc1", 12)
    d2 = create_discount("disc2", 7)
    url = reverse('discounts-list')
    resp = client.get(url)
    assert resp.status_code == 200
    assert d1.name in resp.content.decode()
    assert d2.name in resp.content.decode()
    # контекст
    assert 'discounts' in resp.context
    assert set(resp.context['discounts']) >= {d1, d2}


def test_discount_detail_view(client):
    discount = create_discount("SuperDisc", 15)
    url = reverse('discount_detail', args=[discount.pk])
    resp = client.get(url)
    assert resp.status_code == 200
    assert discount.name in resp.content.decode()
    assert str(discount.percentage) in resp.content.decode()
    # контекст
    assert 'discount' in resp.context
    assert resp.context['discount'] == discount


@pytest.mark.django_db
def test_create_discount_view_get(client):
    url = reverse('create_discount')
    resp = client.get(url)
    assert resp.status_code == 200
    # форма в контексте?
    assert 'form' in resp.context


@pytest.mark.django_db
def test_create_discount_view_post_valid(client, mocker):
    items = create_test_items()
    post_data = {
        "name": "Black Friday",
        "percentage": "25",
        "items": [str(i.pk) for i in items],
    }
    # Мокаем stripe
    mock_coupon = {"id": "fake_stripe_id"}
    mocker.patch("discounts.views.stripe.Coupon.create",
                 return_value=mock_coupon)

    url = reverse("create_discount")
    resp = client.post(url, data=post_data, follow=False)
    # Перенаправление в админку
    assert resp.status_code == 302
    assert resp["Location"].endswith("/admin/discounts/discount/")

    discount = Discount.objects.get(name="Black Friday")
    assert discount.stripe_coupon_id == "fake_stripe_id"
    assert discount.percentage == 25
    assert set(discount.items.all()) == set(items)


@pytest.mark.django_db
def test_create_discount_view_post_invalid(client):
    url = reverse("create_discount")
    # Пустое имя/процент
    resp = client.post(url, data={"name": "", "percentage": ""})
    assert resp.status_code == 200  # форма должна вернуться, а не редирект
    assert "form" in resp.context
    form = resp.context["form"]
    assert form.errors

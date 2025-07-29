from django.core.management.base import BaseCommand
from items.models import Item
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Создаёт случайные товары с помощью Faker'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            nargs='?',
            default=10,
            help='Количество товаров для создания (по умолчанию 10)'
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']
        for _ in range(count):
            item = Item.objects.create(
                name=fake.unique.word().capitalize(),
                description=fake.text(max_nb_chars=200),
                price=round(random.uniform(10, 10000), 2)
            )
            self.stdout.write(self.style.SUCCESS(
                f'Создан товар: {item.name} (цена: {item.price} руб.)'
            ))

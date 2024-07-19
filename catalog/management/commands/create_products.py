from django.core.management import BaseCommand

from catalog.models import Product, Category
from django.utils import timezone


class Command(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()
        category_1 = None
        category_2 = None
        category_3 = None
        category_4 = None

        # Категории: Компьютеры и ноутбуки, Планшеты и мониторы, Смартфоны, Гарнитура
        # можно создать командой: python manage.py create_category

        try:
            category_1 = Category.objects.get(name="Компьютеры и ноутбуки")
        except Category.DoesNotExist:
            category_1 = None
        try:
            category_2 = Category.objects.get(name="Планшеты и мониторы")
        except Category.DoesNotExist:
            category_2 = None
        try:
            category_3 = Category.objects.get(name="Смартфоны")
        except Category.DoesNotExist:
            category_3 = None
        try:
            category_4 = Category.objects.get(name="Гарнитура")
        except Category.DoesNotExist:
            category_4 = None

        product_list = [
            {
                "name": "Ноутбук_Dell",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
                "description": "Описание для ноутбука Dell",
                "price": 100000,
                "product_category": category_1,
            },
            {
                "name": "Ноутбук_Alienware",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
                "description": "Описание для ноутбука Alienware",
                "price": 200000,
                "product_category": category_1,
            },
            {
                "name": "Планшет",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
                "description": "Описание для планшета",
                "price": 10000,
                "product_category": category_2,
            },
            {
                "name": "Телефон",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
                "description": "Описание для телефона",
                "price": 50000,
                "product_category": category_3,
            },
            {
                "name": "Наушники",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
                "description": "Описание для наушников",
                "price": 6000,
                "product_category": category_4,
            },
        ]

        products_for_create = []
        for product_item in product_list:
            products_for_create.append(Product(**product_item))

        Product.objects.bulk_create(products_for_create)

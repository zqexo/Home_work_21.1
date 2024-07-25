import os
from django.core.files import File
from django.core.management import BaseCommand
from django.utils import timezone

from catalog.models import Product, Category


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

        default_images_path = 'media/default/'
        default_images = {
            "Ноутбук_Dell": "dell_default.jpg",
            "Ноутбук_Alienware": "alienware_default.jpg",
            "Планшет": "tablet_default.jpg",
            "Телефон": "phone_default.jpg",
            "Наушники": "headphones_default.jpg",
        }

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

        for product_item in product_list:
            product = Product(**product_item)

            default_image_name = default_images.get(product_item["name"])
            if default_image_name:
                default_image_path = os.path.join(default_images_path, default_image_name)
                if os.path.exists(default_image_path):
                    with open(default_image_path, 'rb') as image_file:
                        product.image_previews.save(default_image_name, File(image_file), save=False)

            product.save()

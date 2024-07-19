from django.core.management import BaseCommand

from catalog.models import Product, Category
from django.utils import timezone


class Command(BaseCommand):

    def handle(self, *args, **options):
        Category.objects.all().delete()
        category_list = [
            {
                "name": "Компьютеры и ноутбуки",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
                "description": "Описание для категории: компьютеры и ноутбуки",
            },
            {
                "name": "Планшеты и мониторы",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
                "description": "Описание для категории: планшеты и электронные книги",
            },
            {
                "name": "Смартфоны",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
                "description": "Описание категории: смартфоны",
            },
            {
                "name": "Гарнитура",
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
                "description": "Описание для категории: гарнитура",
            },
        ]

        category_for_create = []
        for category_item in category_list:
            category_for_create.append(Category(**category_item))

        Category.objects.bulk_create(category_for_create)

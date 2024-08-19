from django.core.cache import cache

from djangoProject2.settings import CACHE_ENABLED
from catalog.models import Product, Category


def get_categories_from_cache():
    """Получаем категории из кэша, если кэш пуст, получаем данные из БД."""
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = "categories_list"
    categories = cache.get(key)
    if categories is not None:
        return categories
    categories = Category.objects.all()
    cache.set(key, categories)
    return categories


def get_products_from_cache():
    """Получаем продукты из кэша, если кэш пуст, получаем данные из БД."""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "products_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products

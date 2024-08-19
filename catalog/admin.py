from django.contrib import admin
from catalog.models import Product, Category, BlogPost, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "price", "product_category")
    list_filter = ("product_category",)
    search_fields = ("name", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "created_at", "published", "views")
    search_fields = ("title", "content")
    list_filter = ("published", "created_at")


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("product", "version_number", "version_name", "version_is_valid")

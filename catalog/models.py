from django.db import models
from django.utils.text import slugify
from django.urls import reverse

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания записи"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения записи"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    image_previews = models.ImageField(
        upload_to="products/", verbose_name="Превью", **NULLABLE
    )
    product_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        **NULLABLE,
        verbose_name="Категория",
    )
    price = models.IntegerField(verbose_name="Цена")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания записи"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения записи"
    )
    views_counter = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )
    is_active = models.BooleanField(default=True, verbose_name="В наличии")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.CharField(max_length=200, **NULLABLE, verbose_name="Slug_url")
    content = models.TextField(verbose_name="Наполнение")
    preview_image = models.ImageField(
        upload_to="blog_previews/", **NULLABLE, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    published = models.BooleanField(default=True, verbose_name="Отображать на сайте")
    views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:blogpost_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ("title",)


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="versions",
        **NULLABLE,
        verbose_name="Продукт",
    )
    version_number = models.IntegerField(default=0, verbose_name="Номер версии")
    version_name = models.CharField(
        max_length=150, **NULLABLE, verbose_name="Название версии"
    )
    version_is_valid = models.BooleanField(
        default=True, verbose_name="Версия актуальна"
    )

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ("product",)

    def __str__(self):
        return f"Version {self.version_number} - {self.version_name}"

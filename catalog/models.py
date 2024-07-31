from django.db import models

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
    name = models.CharField(max_length=100, verbose_name="Наименование", help_text="Введите название")
    description = models.TextField(verbose_name="Описание", **NULLABLE, help_text="Введите описание")
    image_previews = models.ImageField(
        upload_to="products/", verbose_name="Превью", **NULLABLE, help_text="Выберите фото"
    )
    product_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        **NULLABLE,
        verbose_name="Категория",
        help_text="Укажите категорию",
    )
    price = models.IntegerField(verbose_name="Цена", help_text="Укажите цену",)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания записи"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения записи"
    )

    views_counter = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    is_active = models.BooleanField(default=True, verbose_name="В наличии")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)

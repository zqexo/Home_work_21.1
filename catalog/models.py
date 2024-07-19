from django.db import models

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения записи')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    image_previews = models.ImageField(upload_to="students/", verbose_name="Превью", **NULLABLE)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Категория', **NULLABLE)
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения записи')

    is_active = models.BooleanField(default=True, verbose_name="В наличии")
    manufactured_at = models.DateTimeField(null=True, blank=True)  #Поле для удаления

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)

# Generated by Django 5.0.7 on 2024-07-31 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_alter_product_image_previews_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="views_counter",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Количество просмотров"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Введите описание",
                null=True,
                verbose_name="Описание",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image_previews",
            field=models.ImageField(
                blank=True,
                help_text="Выберите фото",
                null=True,
                upload_to="products/",
                verbose_name="Превью",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(
                help_text="Введите название",
                max_length=100,
                verbose_name="Наименование",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.IntegerField(help_text="Укажите цену", verbose_name="Цена"),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_category",
            field=models.ForeignKey(
                blank=True,
                help_text="Укажите категорию",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="catalog.category",
                verbose_name="Категория",
            ),
        ),
    ]

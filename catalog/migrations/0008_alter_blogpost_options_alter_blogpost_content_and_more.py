# Generated by Django 5.0.7 on 2024-08-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_blogpost"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blogpost",
            options={
                "ordering": ("title",),
                "verbose_name": "Публикация",
                "verbose_name_plural": "Публикации",
            },
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="content",
            field=models.TextField(verbose_name="Наполнение"),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата публикации"
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="preview_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="blog_previews/",
                verbose_name="Изображение",
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="published",
            field=models.BooleanField(
                default=False, verbose_name="Отображать на сайте"
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="slug",
            field=models.CharField(
                blank=True, max_length=200, unique=True, verbose_name="Slug_url"
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="title",
            field=models.CharField(max_length=200, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="views",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Количество просмотров"
            ),
        ),
    ]

from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product, Version


class StyleFormMixin:

    def add_bootstrap_classes(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({"class": "form-control-file"})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({"class": "form-check-input"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap_classes()


FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "image_previews",
            "product_category",
            "price",
            "is_active",
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if any(word in name.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Название продукта содержит запрещённые слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description and any(word in description.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Описание продукта содержит запрещённые слова.")
        return description


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = ["product", "version_number", "version_name", "version_is_valid"]

    def clean(self):
        # Почему-то не работает

        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        version_is_valid = cleaned_data.get("version_is_valid")

        if product and version_is_valid is not None:
            if version_is_valid:
                if (
                    Version.objects.filter(product=product, version_is_valid=True)
                    .exclude(id=self.instance.id)
                    .exists()
                ):
                    raise ValidationError(
                        "В один момент может быть только одна активная версия продукта."
                    )

        return cleaned_data

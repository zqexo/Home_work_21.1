from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.models import Product


def contacts(request):
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    message = request.POST.get("message")
    print(f"Имя: {name}, Тел.: {phone}\nСообщение: {message}")
    return render(request, "catalog/contacts.html")


class ProductListView(ListView):
    model = Product
    extra_context = {"title": "Продукты"}


class ProductDetailView(DetailView):
    model = Product
    extra_context = {"title": "Продукт"}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


def register(request):
    return render(request, "catalog/register.html")


class ProductCreateView(CreateView):
    model = Product
    fields = [
        'name',
        'description',
        'image_previews',
        'product_category',
        'price',
        'is_active',
    ]
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = [
        'name',
        'description',
        'image_previews',
        'product_category',
        'price',
        'is_active',
    ]

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get('pk')])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

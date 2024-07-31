from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
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
    context_object_name = "products"
    extra_context = {"title": "Продукты"}


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    extra_context = {"title": "Продукт"}


def register(request):
    return render(request, "catalog/register.html")


class ProductCreateView(CreateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy("catalog:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

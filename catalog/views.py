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
    return render(request, "contacts.html")


class ProductListView(ListView):
    model = Product
    template_name = "products_list.html"
    context_object_name = "products"
    extra_context = {"title": "Продукты"}


class ProductDetailView(DetailView):
    model = Product
    template_name = "products_detail.html"
    context_object_name = "product"
    extra_context = {"title": "Продукт"}


def register(request):
    return render(request, "register.html")


class ProductCreateView(CreateView):
    model = Product
    template_name = "products_form.html"
    fields = "__all__"
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "products_form.html"
    fields = "__all__"
    success_url = reverse_lazy("catalog:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

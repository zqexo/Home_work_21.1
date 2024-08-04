from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from pytils.translit import slugify

from catalog.models import Product, BlogPost


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
        "name",
        "description",
        "image_previews",
        "product_category",
        "price",
        "is_active",
    ]
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = [
        "name",
        "description",
        "image_previews",
        "product_category",
        "price",
        "is_active",
    ]

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("pk")])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "catalog/blogpost_list.html"

    def get_queryset(self):
        return BlogPost.objects.filter(published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "catalog/blogpost_detail.html"
    context_object_name = "blogpost"
    fields = "__all__"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = "catalog/blogpost_form.html"
    fields = ("title", "content", "preview_image", "published")

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = "catalog/blogpost_form.html"
    fields = ("title", "content", "preview_image", "published")

    def get_success_url(self):
        return reverse("catalog:blogpost_detail", args=[self.kwargs.get("pk")])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "catalog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("catalog:blogpost_list")

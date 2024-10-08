from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm, CategoryForm
from catalog.models import Product, BlogPost, Version, Category
from catalog.services import get_products_from_cache, get_categories_from_cache
from django.core.cache import cache


@staff_member_required
def clear_cache_view(request):
    cache.clear()
    return HttpResponse("Cache cleared!")


@login_required
def contacts(request):
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    message = request.POST.get("message")
    print(f"Имя: {name}, Тел.: {phone}\nСообщение: {message}")
    return render(request, "catalog/contacts.html")


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    extra_context = {"title": "Продукты"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = get_categories_from_cache()  # Получаем все категории
        return context

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            category = get_object_or_404(Category, category_slug=category_slug)
            return get_products_from_cache().filter(product_category=category)
        return get_products_from_cache()


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    extra_context = {"title": "Продукт"}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = "catalog.add_product"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    permission_required = "catalog.update_product"

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("pk")])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = ProductFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if formset.is_valid() and form.is_valid:
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_edit_published") and user.has_perm(
            "catalog.can_edit_description"
        ):
            return ProductModeratorForm
        raise PermissionDenied("Недостаточно прав для редактирования этого товара.")


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = "catalog.delete_product"
    success_url = reverse_lazy("catalog:product_list")


class BlogPostListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = "catalog/blogpost_list.html"

    def get_queryset(self):
        return BlogPost.objects.filter(published=True)


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = "catalog/blogpost_detail.html"
    context_object_name = "blogpost"
    fields = "__all__"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    permission_required = "catalog.add_blogpost"
    template_name = "catalog/blogpost_form.html"
    fields = ("title", "content", "preview_image", "published")

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    permission_required = "catalog.update_blogpost"
    template_name = "catalog/blogpost_form.html"
    fields = ("title", "content", "preview_image", "published")

    def get_success_url(self):
        return reverse("catalog:blogpost_detail", args=[self.kwargs.get("pk")])


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    permission_required = "catalog.delete_blogpost"
    template_name = "catalog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("catalog:blogpost_list")


class VersionListView(LoginRequiredMixin, ListView):
    model = Version
    template_name = "catalog/version_list.html"
    context_object_name = "versions"


class VersionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    permission_required = "catalog.add_version"
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy("catalog:version_list")


class VersionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    permission_required = "catalog.update_version"
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy("catalog:version_list")


class VersionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Version
    permission_required = "catalog.delete_version"
    template_name = "catalog/version_confirm_delete.html"
    success_url = reverse_lazy("catalog:version_list")


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "catalog/category_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = get_categories_from_cache()  # Получаем все категории
        return context


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    permission_required = "catalog.add_category"
    template_name = "catalog/category_form.html"
    success_url = reverse_lazy("catalog:category_list")


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    permission_required = "catalog.update_category"
    template_name = "catalog/category_form.html"
    success_url = reverse_lazy("catalog:category_list")


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    permission_required = "catalog.delete_category"
    template_name = "catalog/category_confirm_delete.html"
    success_url = reverse_lazy("catalog:category_list")

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, BlogPost, Version


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


class ProductDetailView(LoginRequiredMixin,  DetailView):
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
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.update_product'

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


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
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


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    permission_required = 'catalog.add_blogpost'
    template_name = "catalog/blogpost_form.html"
    fields = ("title", "content", "preview_image", "published")

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPost
    permission_required = 'catalog.update_blogpost'
    template_name = "catalog/blogpost_form.html"
    fields = ("title", "content", "preview_image", "published")

    def get_success_url(self):
        return reverse("catalog:blogpost_detail", args=[self.kwargs.get("pk")])


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    permission_required = 'catalog.delete_blogpost'
    template_name = "catalog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("catalog:blogpost_list")


class VersionListView(LoginRequiredMixin, ListView):
    model = Version
    template_name = "catalog/version_list.html"
    context_object_name = "versions"


class VersionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    permission_required = 'catalog.add_version'
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy("catalog:version_list")


class VersionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    permission_required = 'catalog.update_version'
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy("catalog:version_list")


class VersionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Version
    permission_required = 'catalog.delete_version'
    template_name = "catalog/version_confirm_delete.html"
    success_url = reverse_lazy("catalog:version_list")

from django.forms import inlineformset_factory
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

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, BlogPost, Version


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
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

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


class VersionListView(ListView):
    model = Version
    template_name = "catalog/version_list.html"
    context_object_name = "versions"


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy("catalog:version_list")


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = "catalog/version_form.html"
    success_url = reverse_lazy("catalog:version_list")



class VersionDeleteView(DeleteView):
    model = Version
    template_name = "catalog/version_confirm_delete.html"
    success_url = reverse_lazy("catalog:version_list")

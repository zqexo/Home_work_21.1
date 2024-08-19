from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import NewappConfig
from catalog.views import (
    contacts,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    VersionListView,
    VersionCreateView,
    VersionDeleteView,
    VersionUpdateView,
    clear_cache_view,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)

app_name = NewappConfig.name

urlpatterns = [
    path("", login_required(ProductListView.as_view()), name="product_list"),
    path(
        "products/<int:pk>/",
        cache_page(60)(ProductDetailView.as_view()),
        name="product_detail",
    ),
    path("contacts/", contacts, name="contact"),
    path("create/", ProductCreateView.as_view(), name="create"),
    path("edit/<int:pk>", ProductUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>", ProductDeleteView.as_view(), name="delete"),
    path("blog/", BlogPostListView.as_view(), name="blogpost_list"),
    path("posts/<int:pk>/", BlogPostDetailView.as_view(), name="blogpost_detail"),
    path("createpost/", BlogPostCreateView.as_view(), name="blogpost_create"),
    path("update/<int:pk>", BlogPostUpdateView.as_view(), name="blogpost_update"),
    path("deletepost/<int:pk>", BlogPostDeleteView.as_view(), name="blogpost_delete"),
    path("versions/", VersionListView.as_view(), name="version_list"),
    path("versions/new/", VersionCreateView.as_view(), name="version_create"),
    path("versions/<int:pk>/edit/", VersionUpdateView.as_view(), name="version_update"),
    path(
        "versions/<int:pk>/delete/", VersionDeleteView.as_view(), name="version_delete"
    ),
    path(
        "products/<slug:category_slug>/",
        ProductListView.as_view(),
        name="product_list_by_category",
    ),
    path("clear-cache/", clear_cache_view, name="clear_cache"),
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/new/", CategoryCreateView.as_view(), name="category_create"),
    path(
        "category/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_update"
    ),
    path(
        "category/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category_delete",
    ),
]

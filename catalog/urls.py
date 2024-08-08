from django.urls import path
from catalog.apps import NewappConfig
from catalog.views import (
    contacts,
    register,
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
)

app_name = NewappConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("contacts/", contacts, name="contact"),
    path("register/", register, name="register"),
    path("create/", ProductCreateView.as_view(), name="create"),
    path("edit/<int:pk>", ProductUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>", ProductDeleteView.as_view(), name="delete"),
    path("blog/", BlogPostListView.as_view(), name="blogpost_list"),
    path("posts/<int:pk>/", BlogPostDetailView.as_view(), name="blogpost_detail"),
    path("createpost/", BlogPostCreateView.as_view(), name="blogpost_create"),
    path("update/<int:pk>", BlogPostUpdateView.as_view(), name="blogpost_update"),
    path("deletepost/<int:pk>", BlogPostDeleteView.as_view(), name="blogpost_delete"),
]

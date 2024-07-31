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
]

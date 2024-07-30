from django.urls import path
from catalog.apps import NewappConfig
from catalog.views import contacts, register, ProductListView, ProductDetailView

app_name = NewappConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("contacts/", contacts, name="contact"),
    path("register/", register, name="register"),
]

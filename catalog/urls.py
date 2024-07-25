from django.urls import path
from catalog.apps import NewappConfig
from catalog.views import contacts, product_list, product_detail, register

app_name = NewappConfig.name

urlpatterns = [
    path("", product_list, name="product_list"),
    path("products/<int:pk>/", product_detail, name='product_detail'),
    path("contacts/", contacts, name="contact"),
    path("register/", register, name="register")
]

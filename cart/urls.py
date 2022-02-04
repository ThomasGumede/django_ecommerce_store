from django.urls import path
from cart.views import cart_details, add_cart, delete_item, update_cart

app_name = "cart"
urlpatterns = [
    path("", cart_details, name="cart_details"),
    path("add/", add_cart, name="add_cart"),
    path("update/", update_cart, name="update_cart"),
    path("delete/", delete_item, name="delete_item")
]

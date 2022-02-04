from django.urls import path
from products.views import product_list_view, product_details_view, add_to_wishlist
app_name = "products"
urlpatterns = [
    path("", product_list_view, name="product_list"),
    path("wish-list/add/", add_to_wishlist, name="add-to-wishlist"),
    path("by-category/<slug:category_slug>/", product_list_view, name="product_by_category"),
    path("product-details/<uuid:product_uuid>/", product_details_view, name="product_details")
]

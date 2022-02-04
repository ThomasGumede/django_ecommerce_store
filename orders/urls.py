from django.urls import path
from orders.views import order_list, create_order, cancel_order, view_order

app_name = "orders"
urlpatterns = [
    path("", order_list, name="order_list"),
    path("create/", create_order, name="create_order"),
    path("view-order/<uuid:order_uuid>/", view_order, name="order"),
    path("delete-order/<uuid:order_uuid>", cancel_order, name="cancel_order")
]

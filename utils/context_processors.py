from django.http import request
from cart.views import get_cart
from products.models import Category

def cart(request):
    return {"cart": get_cart(request)}

def categories(request):
    categories = Category.objects.all()
    return {"categories" : categories}
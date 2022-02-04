from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from cart.cart import Cart

def get_cart(request):
    cart = Cart(request)
    return cart

def cart_details(request):
    cart = get_cart(request)
    return render(request, "cart_details.html", {"cart": cart})

@require_POST
def add_cart(request):
    cart = get_cart(request)
    if request.POST.get("action") == "post":
        product_uuid = request.POST.get("product_uuid", None)
        product_qty = request.POST.get("product_qty", None)
        product = get_object_or_404(Product, product_uuid=product_uuid)

        cart.add(product, int(product_qty))
        
        context = {
            "cart_len": len(cart)
        }

        return JsonResponse(context, status=200)
    else:
        return JsonResponse(status=201)

@require_POST
def update_cart(request):
    cart = get_cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update(product_id, product_qty)

        context = {
            "cart_len": len(cart),
            "total_price": cart.get_total_price()
        }

        return JsonResponse(context, status=200)

@require_POST
def delete_item(request):
    cart = get_cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.remove(product_id)

        context = {
            "cart_len": len(cart),
            "total_price": cart.get_total_price()
        }

        return JsonResponse(context, status=200)
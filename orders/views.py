import weasyprint
from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from cart.views import get_cart
from orders.models import OrderItem, Order
from orders.forms import OrderCreateForm

# Create your views here.
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")

    return render(request, "orders/orders.html", {"orders": orders})


def view_order(request, order_uuid):
    try:
        order = Order.objects.prefetch_related("items").get(order_uuid=order_uuid)
        return render(request, "orders/order_details.html", {"order": order})
    except Order.DoesNotExist:
        print("no")

def create_order(request):
    cart = get_cart(request)
    cart_qty = sum(item['qty'] for item in cart)
    print(cart_qty)
    transport_cost = round((3.99 + (cart_qty // 10) * 1.5), 2)

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            transport = cd['transport']
            
            if transport == 'Recipient pickup':
                transport_cost = 0

            order = form.save(commit=False) 
            order.user = request.user
            order.transport_cost = Decimal(transport_cost) 
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            

            # TODO: Stripe settings

            # Clear cart
            cart.clear()

            return render(request, "orders/order_created.html", {'order': order})
        else:
            return render(request, "orders/create_order.html", {"form": form})
    
    else:
        form = OrderCreateForm()
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'telephone': request.user.phone_number,
                'address1': request.user.address1,
                'address2': request.user.address2,
                'postal_code': request.user.postal_code,
                'city': request.user.city,
                'country': request.user.country,
            }
            order_form = OrderCreateForm(initial=initial_data)

            return render(request, "orders/create_order.html", {"form": order_form})
        else:
            return redirect("accounts:login")

def cancel_order(request, order_uuid):
    order = get_object_or_404(Order, order_uuid=order_uuid)
    if request.user == order.user:
        order.delete()
        

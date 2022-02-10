from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from products.models import Product, Category, Review
from products.forms import ReviewForm


def product_list_view(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category).only("product_uuid", "name", "price", "default_img")
    else:  
        products = Product.objects.only("product_uuid", "name", "price", "default_img")

    context = {
        "products": products
    }

    return render(request, "products/product_list.html", context)

def product_details_view(request, product_uuid):
    try:
        product_qs = Product.objects.prefetch_related("product_images", "reviews").get(product_uuid=product_uuid)

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                review, created = Review.objects.get_or_create(product=product_qs, author=cd["author"], rating=cd["rating"], text=cd["text"])
                if created:
                    review_sr = serializers.serialize("json", [review, ])
                    reviews_count = Review.objects.filter(product=product_qs).count()

                return JsonResponse({"success": True, "review": review_sr, "reviewcount": reviews_count})
            else:
                return JsonResponse({"success": False, "form_errors": form.errors})

        else:
            if request.user.is_authenticated:
                initial_data = {
                    "author": f"{request.user.first_name}"
                }
                review_form = ReviewForm(initial=initial_data)
            else:
                review_form = ReviewForm
            context = {
                "form": review_form,
                "product": product_qs
            }

        return render(request, "products/product_details.html", context)

    except Product.DoesNotExist:
        print("no")

def add_to_wishlist(request):
    if request.method == "POST":
        action = request.POST.get("action", None)
        product_uuid = request.POST.get("product_uuid", None)
        user = request.user
        if action and product_uuid:
            product = get_object_or_404(Product, product_uuid=product_uuid)
            if product not in user.user_wishlist.all() and action == "add":
                user.user_wishlist.add(product)
            else:
                user.user_wishlist.remove(product)
            
            return JsonResponse({"wish_len": user.user_wishlist.count()})
        else:
            return JsonResponse({"error": "Fixxing"})

def product_filtering_view(request):
    product_type = request.GET.get("product_type", None)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Product, Wishlist


def product_list(request):
    query = request.GET.get("q", "").strip()

    products = Product.objects.select_related("category").all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    wishlist_product_ids = []

    if request.user.is_authenticated:
        wishlist_product_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list(
            "product_id",
            flat=True
        )

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "query": query,
            "wishlist_product_ids": wishlist_product_ids,
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product
        }
    )


def about(request):
    return render(
        request,
        'products/about.html'
    )

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related("product")

    return render(
        request,
        "products/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(
            request,
            "Product added to your wishlist."
        )
    else:
        messages.info(
            request,
            "Product is already in your wishlist."
        )

    return redirect('product_list')


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()

    messages.success(
        request,
        "Product removed from your wishlist."
    )

    return redirect('wishlist')
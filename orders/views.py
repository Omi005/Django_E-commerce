from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from cart.models import CartItem
from .models import Order, OrderItem


@login_required
def place_order(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    )

    if not cart_items.exists():
        return redirect('cart')

    order = Order.objects.create(
        user=request.user
    )

    total = 0

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        total += (
            item.product.price *
            item.quantity
        )

    order.total_price = total
    order.save()

    cart_items.delete()

    return redirect('my_orders')

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )

@login_required
def order_detail(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order
        }
    )

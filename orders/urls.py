from django.urls import path
from . import views

urlpatterns = [
    path(
        'place/',
        views.place_order,
        name='place_order'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
    '<int:order_id>/',
    views.order_detail,
    name='order_detail'
),
]
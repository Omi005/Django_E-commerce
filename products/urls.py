from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        '<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),
]
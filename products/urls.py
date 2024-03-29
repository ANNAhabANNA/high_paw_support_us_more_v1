from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path(
        '<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),
    path(
        'add/',
        views.add_inventory,
        name='add_inventory'
    ),
    path(
        'wishlist/add_to_wishlist/<int:product_id>',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),
    path(
        'edit/<int:product_id>/',
        views.edit_inventory,
        name='edit_inventory'
    ),
    path(
        'delete/<int:product_id>/',
        views.delete_inventory,
        name='delete_inventory'
    ),
]

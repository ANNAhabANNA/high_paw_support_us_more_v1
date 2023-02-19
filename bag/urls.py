from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_bag, name='review_bag'),
    path('add/<item_id>/', views.add_product, name='add_product'),
    path('adjust/<item_id>/', views.adjust_product, name='adjust_product'),
    path('remove/<item_id>/', views.remove_product, name='remove_product'),
]

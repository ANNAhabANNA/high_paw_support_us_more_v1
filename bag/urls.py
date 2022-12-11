from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_bag, name='review_bag')
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_comments, name='all_comments'),
    path('add_comment/', views.AddReview.as_view(), name='add_comment'),
]

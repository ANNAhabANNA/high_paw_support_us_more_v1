from django.urls import path
from .import views
from .views import BlogList


urlpatterns = [
    path('', BlogList.as_view(), name='blog'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]

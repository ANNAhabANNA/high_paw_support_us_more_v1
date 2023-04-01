from django.urls import path
from .import views
from .views import BlogList


urlpatterns = [
    path('', BlogList.as_view(), name='blog'),
]

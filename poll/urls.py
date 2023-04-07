from django.contrib import admin
from django.urls import path

from poll import views as poll_views

urlpatterns = [
    path('', poll_views.home, name='poll'),
    path('create/', poll_views.create, name='create'),
    path('vote/<poll_id>/', poll_views.vote, name='vote'),
    path('results/<poll_id>/', poll_views.results, name='results'),
]
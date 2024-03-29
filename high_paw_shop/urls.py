"""high_paw_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    custom_403_error,
    custom_404_error,
    custom_500_error,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Allauth
    path('accounts/', include('allauth.urls')),
    # Home page
    path('', include('home.urls')),
    # Products page
    path('products/', include('products.urls')),
    # Shopping bag page
    path('bag/', include('bag.urls')),
    # Checkout page
    path('checkout/', include('checkout.urls')),
    # User profile page
    path('profile/', include('profiles.urls')),
    # Reviews page
    path('reviews/', include('reviews.urls')),
    # Subscription page
    path('subscription/', include('marketing.urls')),
    # Blog page
    path('blog/', include('blog.urls')),
    path('poll/', include('poll.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'high_paw_shop.views.custom_403_error'
handler404 = 'high_paw_shop.views.custom_404_error'
handler500 = 'high_paw_shop.views.custom_500_error'

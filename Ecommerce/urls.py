"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('products/admin/',include('Ecommerce.admin_panel.products.urls')),
    path('inventory/admin/',include('Ecommerce.admin_panel.inventory.urls')),
    path('user/admin/',include('Ecommerce.admin_panel.users.urls')),
    path('orders/admin/',include('Ecommerce.admin_panel.orders.urls')),
    path('dashboard/admin/',include('Ecommerce.admin_panel.dashboard.urls')),
    path('advertisement/admin/',include('Ecommerce.admin_panel.advertisement.urls')),
    path('messages/',include('Ecommerce.admin_panel.client_messages.urls')),
    path('',include('Ecommerce.client_panel.homepage.urls')),
    path('products/',include('Ecommerce.client_panel.client_products.urls')),
    path('user/',include('Ecommerce.client_panel.client_signup.urls')),
    path('profile/',include('Ecommerce.client_panel.client_profile.urls')),
    path('cart/',include('Ecommerce.client_panel.cart.urls')),
    path('order/',include('Ecommerce.client_panel.client_order.urls')),
    path('wishlist/',include('Ecommerce.client_panel.wishlist.urls')),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


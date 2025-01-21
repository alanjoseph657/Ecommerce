from django.urls import path

from Ecommerce.client_panel.client_products.views import products_view
from Ecommerce.client_panel.client_products.views import more_products
from Ecommerce.client_panel.client_products.views import product_detail_view

urlpatterns = [
    path('shop/', products_view, name='products_view'),
    path('more_products/', more_products, name='more_products'),
    path('<slug:slug>/', product_detail_view, name='product_detail_view'),
]
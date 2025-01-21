from django.urls import path

from Ecommerce.client_panel.client_order.views import payment_page_view
from Ecommerce.client_panel.client_order.views import place_order_views
from Ecommerce.client_panel.client_order.views import client_orders_view
from Ecommerce.client_panel.client_order.views import order_detail_view
from Ecommerce.client_panel.client_order.views import cancel_order_view


urlpatterns = [
    path('payment_page/', payment_page_view, name="payment_page"),
    path('place_order/', place_order_views, name="place_order"),
    path('client_orders/', client_orders_view, name="client_orders"),
    path('client_order_detail/', order_detail_view, name="client_order_detail"),
    path('cancel_order/', cancel_order_view, name="cancel_order"),
]
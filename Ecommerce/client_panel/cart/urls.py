from django.urls import path

from Ecommerce.client_panel.cart.views import cart_page_view
from Ecommerce.client_panel.cart.views import remove_from_cart_view
from Ecommerce.client_panel.cart.views import get_address_by_id_for_cart_view
from Ecommerce.client_panel.cart.views import proceed_checkout_view


urlpatterns = [ 
    path('user_cart/', cart_page_view, name="cart"),
    path('remove_from_cart_view/', remove_from_cart_view, name="remove_from_cart_view"),
    path('get_address_by_id_for_cart_view/', get_address_by_id_for_cart_view, name="get_address_by_id_for_cart_view"),
    path('proceed_checkout_view/', proceed_checkout_view, name="proceed_checkout_view"),
]
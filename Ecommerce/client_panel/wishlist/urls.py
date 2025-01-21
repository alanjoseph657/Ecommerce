from django.urls import path

from Ecommerce.client_panel.wishlist.views import get_wishlist_view
from Ecommerce.client_panel.wishlist.views import add_to_wishlist_view
from Ecommerce.client_panel.wishlist.views import remove_from_wislist_view


urlpatterns = [
    path('wishlist/',get_wishlist_view, name="wishlist"),
    path('add_to_wishlist_view/',add_to_wishlist_view, name="add_to_wishlist_view"),
    path('remove_from_wislist/',remove_from_wislist_view, name="remove_from_wislist"),
]
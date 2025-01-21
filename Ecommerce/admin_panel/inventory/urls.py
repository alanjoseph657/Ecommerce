from django.urls import path

from Ecommerce.admin_panel.inventory.views import list_inventory_view
from Ecommerce.admin_panel.inventory.views import inventory_list_by_product_search_view
from Ecommerce.admin_panel.inventory.views import update_inventory_view

urlpatterns = (
    path('list_inventory/', list_inventory_view, name='list_inventory'),
    path('inventory_list_by_product_search/', inventory_list_by_product_search_view, name='inventory_list_by_product_search'),
    path('update_inventory/<int:inventory_id>/', update_inventory_view, name='update_inventory'),
)
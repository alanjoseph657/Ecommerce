from django.urls import path

from Ecommerce.admin_panel.dashboard.views import dashboard_view
from Ecommerce.admin_panel.dashboard.views import get_inventory_chart


urlpatterns = [
    path('', dashboard_view, name='dashboard_view'),
    path('get_inventory_chart/', get_inventory_chart, name='get_inventory_chart'),

]
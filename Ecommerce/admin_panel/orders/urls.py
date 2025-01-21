from django.urls import path


from Ecommerce.admin_panel.orders.views import list_order_view
from Ecommerce.admin_panel.orders.views import list_order_status_filter_view
from Ecommerce.admin_panel.orders.views import search_order_by_number_view
from Ecommerce.admin_panel.orders.views import order_detail_view
from Ecommerce.admin_panel.orders.views import view_order_by_product
from Ecommerce.admin_panel.orders.views import order_by_product


urlpatterns = (
        path('orders/', list_order_view, name='orders'),
        path('list_order_status_filter/<str:status>/', list_order_status_filter_view, name='list_order_status_filter'),
        path('search_order_by_number/', search_order_by_number_view, name='search_order_by_number'),
        path('order_detail/<int:order_id>/', order_detail_view, name='order_detail'),
        path('order_by_product/', view_order_by_product, name='order_by_product'),
        path('search_order_by_product/', order_by_product, name='search_order_by_product'),

)
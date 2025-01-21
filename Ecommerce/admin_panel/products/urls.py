from django.urls import path

from Ecommerce.admin_panel.products.views import create_category_view
from Ecommerce.admin_panel.products.views import list_all_categories_view
from Ecommerce.admin_panel.products.views import update_category_view
from Ecommerce.admin_panel.products.views import delete_category_view
from Ecommerce.admin_panel.products.views_v2 import add_product_view
from Ecommerce.admin_panel.products.views_v2 import list_all_products_view
from Ecommerce.admin_panel.products.views_v2 import product_detail_view
from Ecommerce.admin_panel.products.views_v2 import update_variant_view
from Ecommerce.admin_panel.products.views_v2 import add_variant_view
from Ecommerce.admin_panel.products.views_v2 import delete_variant_view
from Ecommerce.admin_panel.products.views_v2 import update_product_data_view
from Ecommerce.admin_panel.products.views_v2 import edit_product_detail_form
from Ecommerce.admin_panel.products.views_v2 import edit_product_gallery_form
from Ecommerce.admin_panel.products.views_v2 import search_product_name_view
from Ecommerce.admin_panel.products.views_v2 import product_status_change_view
from Ecommerce.admin_panel.products.views_v2 import product_search_suggestions_view
from Ecommerce.admin_panel.products.views_v2 import delete_product_view


urlpatterns = (
    path('create_category/', create_category_view, name='create_category'),
    path('list_all_categories/', list_all_categories_view, name='list_all_categories'),
    path('update_category/<slug:slug>/', update_category_view, name='update_category'),
    path('delete_category/<slug:slug>/', delete_category_view, name='delete_category'),
    path('list_all_products/', list_all_products_view, name='list_all_products'),
    path('list_all_products/<int:category_id>/', list_all_products_view, name='list_all_products_with_category'),
    path('product_detail/<slug:slug>/', product_detail_view, name='product_detail'),
    path('add_product/', add_product_view, name='add_product'),
    path('update_variant/', update_variant_view, name='update_variant'),
    path('add_variant/<int:product_id>/', add_variant_view, name='add_variant'),
    path('delete_variant/<int:variant_id>/', delete_variant_view, name='delete_variant'),
    path('update_product/<slug:slug>/', update_product_data_view, name='update_product'),
    path('edit_product_detail_form/<int:product_id>/', edit_product_detail_form, name='edit_product_detail_form'),
    path('edit_product_gallery_form/<int:product_id>/', edit_product_gallery_form, name='edit_product_gallery_form'),
    path('search_product_name/', search_product_name_view, name='search_product_name'),
    path('product_status_change/', product_status_change_view, name='product_status_change'),
    path('product_search_suggestions/', product_search_suggestions_view, name='product_search_suggestions'),
    path('delete_product/<slug:slug>/', delete_product_view, name='delete_product'),
)
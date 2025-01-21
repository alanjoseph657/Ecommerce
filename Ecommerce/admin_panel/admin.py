from django.contrib import admin

from Ecommerce.dataaccess.ecommerce_access.product_models import Categories
from Ecommerce.dataaccess.ecommerce_access.product_models import Products
from Ecommerce.dataaccess.ecommerce_access.product_models import ProductMedia
from Ecommerce.dataaccess.ecommerce_access.product_models import ProductVariant
from Ecommerce.dataaccess.ecommerce_access.inventory_models import Inventory
from Ecommerce.dataaccess.ecommerce_access.inventory_models import InventoryHistory
from Ecommerce.dataaccess.ecommerce_access.inventory_models import CartReservation
from Ecommerce.dataaccess.ecommerce_access.order_models import Order
from Ecommerce.dataaccess.ecommerce_access.order_models import OrderItem
from Ecommerce.dataaccess.ecommerce_access.order_models import OrderHistory
from Ecommerce.dataaccess.ecommerce_access.user_models import ShippingAddress
from Ecommerce.dataaccess.ecommerce_access.user_models import ClientReport


admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(ProductMedia)
admin.site.register(ProductVariant)
admin.site.register(Inventory)
admin.site.register(InventoryHistory)
admin.site.register(CartReservation)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderHistory)
admin.site.register(ShippingAddress)
admin.site.register(ClientReport)
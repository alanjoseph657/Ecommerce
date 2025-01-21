import json

from django.utils import timezone

from Ecommerce.dataaccess.ecommerce_access.inventory_da import CartDA
from Ecommerce.dataaccess.ecommerce_access.inventory_da import InventoryDA
from Ecommerce.dataaccess.ecommerce_access.order_da import OrderDA


class CartBl():
    def __init__(self):
        pass

    def add_product_to_cart_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant')
        quantity = request.POST.get('quantity')

        try:
            cart_dict = {
                'product_id' : product_id,
                'variant_id' : variant_id,
                'quantity' : quantity
            }

            check_cart = CartDA().get_cart_by_user(user_id).filter(variant_id=variant_id)

            if check_cart.exists():
                CartDA().update_item_quantity_in_cart(user_id, cart_dict)

            else:
                CartDA().add_to_cart(user_id, cart_dict)

            inventory = InventoryDA().update_inventory_by_reservation(variant_id, int(quantity))

            response['success'] = True
            response['msg'] = "Product added to cart successfully"
        except Exception as err:
            response['error'] = str(err)
        
        return response
    
    def get_cart_for_user_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id

        try:
            cart = CartDA().get_cart_by_user(user_id)
            for item in cart:
                if item.status == 'EXPIRED':
                    InventoryDA().update_inventory_by_reservation(item.variant_id, item.quantity)
                item.reserved_at = timezone.now()
                item.save()
            update_cart = cart.update(status = 'RESERVED')
            response['success'] = True
            response['cart_items'] = cart
        except Exception as err:
            response['error'] = "Unable to fetch cart"
        return response
    
    def remove_from_cart_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        cart_id = request.GET.get('cart_id')

        try:
            check_status = CartDA().get_cart_record_by_cart_id(cart_id)
            InventoryDA().update_inventory_on_reservation_expiry(check_status.variant_id, check_status.quantity)
            cart = CartDA().remove_with_cart_id(cart_id)
            response['success'] = True
        except Exception as err:
            response['error'] = "Unable to remove item from cart"
        return response
    
    def proceed_checkout_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        data = json.loads(request.body)
        user_id = request.user.id
        cart_items = data['cart_items']
        shipping_address_id = data['shipping_address_id']
        total_price = data['total_price']
        cart_id = data['cart_item_ids']

        try:
            order_dict = {
                'user_id': user_id,
                'total_price' : total_price,
                'shipping_address_id' : shipping_address_id
            }

            order = OrderDA().create_new_order(order_dict)

            for item in cart_items:
                item_dict = {
                'order': order.id,
                'product_id': item['product_id'],
                'variant_id': item['variant_id'],
                'quantity': item['quantity'],
                'price': item['price']
                }
                OrderDA().add_item_to_order(item_dict)
            
            for id in cart_id:
                CartDA().update_reservation_on_order(id)

            response['success'] = True
            response['msg'] = "Order placed {order.id}"
            response['order_id'] = order.id
        
        except Exception as err:
            response['error'] = "Failed to place order"
        
        return response
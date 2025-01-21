from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Ecommerce.dataaccess.ecommerce_access.order_da import OrderDA
from Ecommerce.dataaccess.ecommerce_access.user_da import AddressDA
from Ecommerce.dataaccess.ecommerce_access.user_da import UserDA
from Ecommerce.common.utilities import order_confirmation_mail


class OrderBL():
    def __init__(self):
        pass

    def place_order_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        order_id = request.GET.get('order_id')

        try:
            order = OrderDA().get_order_details_by_id(order_id)
            order_items = OrderDA().get_all_items_by_order_id(order_id)
            email = UserDA().get_user_email(order.user_id)

            order_dict = {
                'order_id' : order.id,
                'status': order.status
            }

            for items in order_items:
                order_dict['product_id'] = items.product_id
                order_dict['variant_id'] = items.variant_id
                OrderDA().create_order_history(order_dict)
            
            order_confirmation_mail(email, order.id)
            response['success'] = True
        
        except Exception as err:
            response['error'] = "No orders Found"
        
        return response
    
    def get_orders_by_user_bl(self, request, item_per_page = 3):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        page = request.GET.get('page', 1)

        try:
            orders = OrderDA().get_orders_by_user(user_id)
            paginator = Paginator(orders, item_per_page)
            paginated_orders = paginator.page(page)
            
            response['success'] = True
            response['orders'] = paginated_orders

        except Exception as err:
            response['error'] = "No orders placed yet"
        
        return response
    
    def get_order_detail_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        order_id = request.GET.get('order_id')

        try:
            order = OrderDA().get_order_details_by_id(order_id)
            address = AddressDA().get_address_by_id(order.shipping_address_id)
            items = OrderDA().get_order_items_with_product_media_and_variant(order_id)
            response['success'] = True
            response['items'] = items
            response['order'] = order
            response['address'] = address
        except Exception as err:
            response['error'] = "No record found"
        return response
    
    def cancel_order_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        order_id = request.GET.get('order_id')

        try:
            OrderDA().update_order_history(order_id, status='CANCELLED')
            OrderDA().cancel_order(order_id)
            response['success'] = True
            response['msg'] = "Order Cancelled"            
        except Exception as err:
            response['error'] = "Failed to cancel the order"
        return response
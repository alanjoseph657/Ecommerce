from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from Ecommerce.dataaccess.ecommerce_access.order_da import OrderDA
from Ecommerce.dataaccess.ecommerce_access.user_da import AddressDA
from Ecommerce.dataaccess.ecommerce_access.user_da import UserDA
from Ecommerce.dataaccess.ecommerce_access.product_da import ProductDA


class OrderBL():
    def __init__(self):
        pass

    def list_all_orders_bl(self, request, item_per_page=10):
        response = {"error": None, "success": False, "msg": "", "paginated_products": None}
        page_number = request.GET.get('page',1)  
        status = request.GET.get('order_status')
        search_number = request.GET.get('search_number')

        try:
            if search_number:
                if status:
                    orders = OrderDA().filter_order_with_id(query=search_number, status=status)
                else:
                    orders = OrderDA().filter_order_with_id(query=search_number)
            else:
                if status:
                    orders = OrderDA().get_orders_by_status(status.upper()).order_by('-created_at')

                else:
                    orders = OrderDA().get_all_orders().order_by('-created_at')
            if orders:
                if 'search_number' in request.session:
                    number = request.session.get('search_number')
                    orders = orders.filter(id__contains=number)
                    
                paginator = Paginator(orders, item_per_page)
                try:
                    paginated_orders = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_orders = paginator.page(1)
                except EmptyPage:
                    paginated_orders = paginator.page(paginator.num_pages)
                response["paginated_orders"] = paginated_orders
                response["success"] = True 
            else:
                response['error'] = "No Orders Found"
        except Exception as err:
            response['error'] = str(err)
        return response
    

    def search_orders_by_reference(self, request, item_per_page=10):
        response = {"error": None, "success": False, "msg": ""}
        page_number = request.GET.get('page',1)

        if 'search_number' in request.session:
            query = request.session.get('search_number', '')
        else: 
            query = request.POST.get('search-number')
            request.session['search_number'] = query

        try:
            orders = OrderDA().filter_order_with_id(query)
            if orders:
                paginator = Paginator(orders, item_per_page)
                try:
                    paginated_orders = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_orders = paginator.page(1)
                except EmptyPage:
                    paginated_orders = paginator.page(paginator.num_pages)
                response["paginated_orders"] = paginated_orders
                response["success"] = True 
            else:
                response['error'] = "No Orders Found"
        except Exception as err:
            response['error'] = str(err)
        return response

    def order_detail_bl(self, order_id):
        response = {"error": None, "success": False, "msg": "", "paginated_products": None}
        try:
            order = OrderDA().get_order_details_by_id(order_id)
            order_item = OrderDA().get_orders_with_product_and_variant(order_id)
            address = AddressDA().get_address_by_id(order.shipping_address_id)
            user = UserDA().get_user_by_id(order.user_id)
            response['success'] = True
            response['order'] = order
            response['orderitem'] = order_item
            response['user'] = user
            response['address'] = address
        except Exception as err:
            response['error'] = "Failed to get order details"
        return response
    
    def order_list_by_product_bl(self, request, query, item_per_page=10):
        response = {"error": None, "success": False, "msg": "", "paginated_products": None}
        page_number = request.GET.get('page',1)  
        products = ProductDA().search_product_using_name_for_order(query)

        if products:
            try:
                orders=[]
                for product in products:
                    orders.extend(OrderDA().get_orders_by_product(product.id))

                if orders:
                    paginator = Paginator(orders, item_per_page)
                    try:
                        paginated_orders = paginator.page(page_number)
                    except PageNotAnInteger:
                        paginated_orders = paginator.page(1)
                    except EmptyPage:
                        paginated_orders = paginator.page(paginator.num_pages)
                    response["paginated_orders"] = paginated_orders
                    response["success"] = True 
                else:
                    response['error'] = "No Orders Found"
            except Exception as err:
                response['error'] = "An error occured"
        else:
            response['error'] = "Invaid Product"
        
        return response

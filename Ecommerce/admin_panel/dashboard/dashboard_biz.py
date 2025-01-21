from datetime import timedelta
from django.utils import timezone
from collections import defaultdict

from Ecommerce.dataaccess.ecommerce_access.inventory_da import InventoryDA
from Ecommerce.dataaccess.ecommerce_access.product_da import ProductDA
from Ecommerce.dataaccess.ecommerce_access.order_da import OrderDA
from Ecommerce.dataaccess.ecommerce_access.user_da import UserDA
from Ecommerce.dataaccess.ecommerce_access.user_da import ClientReportDA



class DashboardBL():
    def __init__(self):
        pass

    def count_cards_bl(self):
        response = {"error": None, "success": False, "msg": ""}
        try:
            inventory_count = InventoryDA().get_available_inventory_total()
            products_count = ProductDA().get_active_products().count()
            orders_count = OrderDA().get_all_orders().count()
            users = UserDA().get_all_clients().count()
            
            response['inventory_count'] = inventory_count
            response['products_count'] = products_count
            response['orders_count'] = orders_count
            response['users'] = users
            response['success'] = True
        except Exception as err:
            response['error'] = str(err)

        return response
    
    def recent_inventory_actions_bl(self):
        response = {"error": None, "success": False, "msg": ""}
        try:
            recent_history = InventoryDA().get_recent_history()
            response["success"] = True
            response['recent_history'] = recent_history
        
        except Exception as err:
            response['error'] = str(err)

        return response

    def history_for_7_days(self, select_days = 7):
        response = {"error": None, "success": False, "msg": ""}

        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=select_days)
            history_data = InventoryDA().get_history_for_7_days(start_date, end_date)

            date_dict = defaultdict(int)

            for data in history_data:
                date_dict[data['date'].date()] = data['total_change']

            history_graph = []
            current_date = start_date.date()
            while current_date <= end_date.date():
                history_graph.append({
                    "date": current_date.strftime('%Y-%m-%d'),
                    "total_change": date_dict[current_date]
                })
                current_date += timedelta(days=1)
            
            response['success'] = True     
            return history_graph
        
        except Exception as err:
            response['error'] = str(err)
        
            return response
        
    def dashboard_client_reports_bl(self):
        response = {"error": None, "success": False, "msg": ""}
        try:
            reports = ClientReportDA().client_report_for_dashboard()
            response['success'] = True
            response['reports'] = reports
        except Exception as err:
            response['error'] = str(err)
        
        return response
    
    def dashboard_products_bl(self):
        response = {"error": None, "success": False, "msg": ""}
        try:
            products = ProductDA().get_all_products_data()[:5]
            response['success'] = True
            response['products'] = products
        except Exception as err:
            response['error'] = str(err)
        return response

    def most_ordered_product_bl(self):
        response = {"error": None, "success": False, "msg": ""}
        try:
            product_id = OrderDA().most_ordered_product()
            product_details = ProductDA().get_product_details_by_id(product_id['product_id'])
            product_media = ProductDA().get_product_media(product_id['product_id']).first()
            response['success'] = True
            response['product_details'] = product_details
            response['product_media'] = product_media
        except Exception as err:
            response['error'] = str(err)

        return response
    
    def order_status_bl(self):
        response = {"error": None, "success": False, "msg": ""}
        try:
            order_status_counts = OrderDA().get_order_status_chart()
            order_status_data = {
                'labels': [item['status'] for item in order_status_counts],
                'data': [item['count'] for item in order_status_counts]
            }
            response['success'] = True
            response['order_status'] = order_status_data
        except Exception as err:
            response['error'] = str(err)
        return response
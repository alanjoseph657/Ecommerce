from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from Ecommerce.dataaccess.ecommerce_access.inventory_da import InventoryDA
from Ecommerce.dataaccess.ecommerce_access.product_da import ProductDA


class InventoryBL():

    def __init__(self):
        pass

    def get_inventory_list_bl(self, request, item_per_page=10):
        page_number = request.GET.get('page', 1)
        response = {"error": None, "success": False, "msg": "","paginated_inventory": None, "products" : None,
                    "inventory_count": None, "variants": None}
        query = request.GET.get('search_query')
        try:
            
            if query:
                inventory = []
                products = ProductDA().search_product_using_name_for_order(query)
                for product in products:
                    inventory.extend(InventoryDA().get_inventory_with_product_id_and_variant(product.id))
                
            else:
                inventory = InventoryDA().get_inventory_with_product_and_variant()

            products = ProductDA().get_active_products().count()
            inventory_count = InventoryDA().get_available_inventory_total()
            variants = ProductDA().get_all_variants().count()

            if inventory:
                paginator = Paginator(inventory, item_per_page)
                try:
                    paginated_inventory = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_inventory = paginator.page(1)
                except EmptyPage:
                    paginated_inventory = paginator.page(paginator.num_pages)
                response['paginated_inventory'] = paginated_inventory
                response['products'] = products
                response['inventory_count'] = inventory_count
                response['variants'] = variants
            else:
                response['error'] = "No inventory records found"
        except Exception as err:
            response['error'] = str(err)
        return response

    def update_inventory_record_bl(self, request, inventory_id):
        response = {"error": None, "success": False, "msg": ""}
        stock = request.POST.get('stock')
        reorder_level = request.POST.get('reorder_level')

        data_dict = {
            'stock' : stock,
            'reorder_level' : reorder_level
        }
        try:
            InventoryDA().update_inventory(inventory_id, data_dict)
            self.save_inventory_history(inventory_id)
            response['success'] = True
            response['msg'] = "Inventory Record Updated"

        except Exception as err:
            response['error'] = "An Error Occured while updating"

        return response
    
    def get_inventory_data_bl(self, inventory_id):
        response = {"error": None, "success": False, "msg": ""}
        try:
            inventory = InventoryDA().get_inventory_record_with_product_and_variant(inventory_id)
            inventory = list(inventory)
            response['inventory'] =inventory[0]
            response['success'] = True
        except Exception as err:
            response['error'] = "Failed to fetch data"
        return response
    
    def save_inventory_history(self, inventory_id):
        response = {"error": None, "success": False, "msg": ""}
        inventory = InventoryDA().get_inventory_by_inventory_id(inventory_id)

        try:
            latest_history = InventoryDA().get_latest_history(inventory.variant_id)
            
            if latest_history:
                if inventory.stock != latest_history.new_stock:
                    change = inventory.stock - latest_history.new_stock
                    note = (f'Inventory updated. Previous stock: {latest_history.new_stock}. '
                            f'New stock: {inventory.stock}')
                else:
                    response['success'] = True
                    response['msg'] = "No changes in stock"
                    return response
            else:
                change = inventory.stock
                note = f'New stock added. New stock: {inventory.stock}'

            data_dict = {
                'product_id': inventory.product_id,
                'variant_id': inventory.variant_id,
                'new_stock': inventory.stock,
                'change': change,
                'note': note
            }
            
            InventoryDA().add_new_history(data_dict)
            response['success'] = True
            response['msg'] = "Inventory History Record Saved"

        except Exception as err:
            response['error'] = "Failed to save history"

        return response
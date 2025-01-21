from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, Sum, Subquery, CharField, OuterRef, Value, DecimalField
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncDay 

from Ecommerce.dataaccess.ecommerce_access.inventory_models import Inventory
from Ecommerce.dataaccess.ecommerce_access.inventory_models import InventoryHistory
from Ecommerce.dataaccess.ecommerce_access.inventory_models import CartReservation
from Ecommerce.dataaccess.ecommerce_access.product_models import ProductMedia, Products
from Ecommerce.dataaccess.ecommerce_access.product_models import ProductVariant


class InventoryDA():

    def __init__(self):
        pass

    def get_inventory(self):
        return Inventory.objects.all()
    
    def get_available_inventory(self):
        return Inventory.objects.filter(deleted=False)
    
    def get_available_inventory_total(self):
        return Inventory.objects.filter(deleted=False).aggregate(total_stock=Sum('stock'))['total_stock']
    
    def get_inventory_by_product(self, product_id):
        return Inventory.objects.filter(product_id=product_id)
    
    def get_inventory_by_inventory_id(self, inventory_id):
        return get_object_or_404(Inventory, id=inventory_id)
    
    def get_inventory_by_inventory_variant(self, variant_id):
        return get_object_or_404(Inventory, variant_id=variant_id)
    
    def get_recent_history(self):
        history = InventoryHistory.objects.raw(
            '''
            SELECT history.* , product.product_name AS product_name,
            variant.variant_name AS variant_name
            FROM ecommerce_access_inventoryhistory AS history
            LEFT JOIN ecommerce_access_products AS product
            ON history.product_id = product.id
            LEFT JOIN ecommerce_access_productvariant as variant
            ON history.variant_id = variant.id
            ORDER BY history.created_at DESC
            LIMIT 5;
        '''
        )

        return history
    
    def get_history_for_7_days(self, start_date, end_date):
        return InventoryHistory.objects.filter(
            created_at__range=[start_date, end_date]
        ).annotate(
            date=TruncDay('created_at')
        ).values(
            'date'
        ).annotate(
            total_change=Sum('change')
        ).order_by('date')

    
    def get_inventory_history_by_product(self, product_id):
        return InventoryHistory.objects.filter(product_id=product_id).order_by('created_at')

    def get_inventory_history_by_variant(self, variant_id):
        return InventoryHistory.objects.filter(variant_id=variant_id).order_by('created_at')
    
    def get_inventory_history_by_inventory_id(self, inventory_id):
        return InventoryHistory.objects.filter(inventory_id=inventory_id).order_by('created_at')
    
    def get_inventory_history_by_date(self, inventory_id, start_date, end_date):
        return InventoryHistory.objects.filter(
            Q(inventory_id=inventory_id) & Q(created_at__gte=start_date) & Q(created_at__lte=end_date)
            ).order_by('created_at')
    
    def add_new_record(self, data_dict):
        try:
            return Inventory.objects.create(**data_dict)
        except Exception as err:
            return str(err)
        
    def update_product_inventory(self):
        total_stock = Inventory.objects.filter(
            product_id=self.product_id).aggregate(total_stock=Sum('stock'))['total_stock'] or 0
        Products.objects.filter(id=self.product_id).update(inventory=total_stock)

    def update_inventory(self, inventory_id, data_dict):
        try:
            updated = Inventory.objects.filter(id=inventory_id).update(**data_dict)

            if updated == 0:
                raise Inventory.DoesNotExist(f'Inventory with id {inventory_id} does not exist.')
        except Exception as err:
            return str(err)
        return updated
    
    def update_inventory_for_variant(self, variant_id, data_dict):
        try:
            updated = Inventory.objects.filter(variant_id=variant_id).update(**data_dict)

            if updated == 0:
                raise Inventory.DoesNotExist(f'Inventory for variant {variant_id} does not exist.')
        except Exception as err:
            return str(err)
        return updated
        
    def update_stock_for_variant(self, variant_id, data_dict):
        try:
            record = Inventory.objects.filter(variant_id=variant_id)
            if record.exists():
                record.update(**data_dict)
                record = record.first()
            else:
                record = Inventory.objects.create(variant_id=variant_id, **data_dict)
                ProductVariant.objects.filter(id= variant_id).update(inventory_id = record.id)
            return record
        except Exception as err:
            return str(err)
    
    def add_new_history(self, data_dict):
        try:
            return InventoryHistory.objects.create(**data_dict)
        except Exception as err:
            return str(err)

    def get_latest_history(self, variant_id):
        return InventoryHistory.objects.filter(variant_id=variant_id).order_by('-created_at').first()
    
    def update_inventory_by_reservation(self, variant_id, quantity):
        inventory = Inventory.objects.filter(variant_id=variant_id).first()
        
        if inventory:
            inventory.stock -= quantity
            inventory.save()
        else:
            return f'Inventory record for product ID {variant_id} does not exist.'
        return inventory
    
    def update_inventory_on_reservation_expiry(self, variant_id, quantity):
        inventory = Inventory.objects.filter(variant_id=variant_id).first()
        
        if inventory:
            inventory.stock += quantity
            inventory.save()
        else:
            return f'Inventory record for product ID {variant_id} does not exist.'
        return inventory
    
    def delete_inventory_record(self, inventory_id):
        deleted_count = Inventory.objects.filter(id=inventory_id).update(deleted= True)
        
        if deleted_count > 0:
            return f'Inventory record with id {inventory_id} has been deleted.'
        else:
            return f'No Inventory record found with id {inventory_id}.'
        
    def delete_inventory_records_by_product(self, product_id):
        deleted_count = Inventory.objects.filter(product_id=product_id).update(deleted= True)
        
        if deleted_count > 0:
            return f'Inventory record with product id {product_id} has been deleted.'
        else:
            return f'No Inventory record found for product {product_id}.'
        
    def get_inventory_with_product_and_variant(self):
        inventory = Inventory.objects.raw('''
        SELECT inventory.*, product.product_name AS product_name,
                product.slug AS slug,
                variant.variant_name AS variant_name           
                FROM ecommerce_access_inventory AS inventory
                LEFT JOIN ecommerce_access_products AS product
                ON inventory.product_id = product.id
                LEFT JOIN ecommerce_access_productvariant AS variant
                ON inventory.variant_id = variant.id
                WHERE inventory.deleted = false
                ORDER BY inventory.product_id DESC;
        ''')
        return inventory
    
    def get_inventory_record_with_product_and_variant(self, inventory_id):
        inventory = Inventory.objects.raw('''
        SELECT inventory.*, product.product_name AS product_name,
                product.slug AS slug,
                variant.variant_name AS variant_name           
                FROM ecommerce_access_inventory AS inventory
                LEFT JOIN ecommerce_access_products AS product
                ON inventory.product_id = product.id
                LEFT JOIN ecommerce_access_productvariant AS variant
                ON inventory.variant_id = variant.id
                WHERE inventory.id = %s;
        ''',[inventory_id])
        return inventory
    
    def get_inventory_with_product_id_and_variant(self, query):
        inventory = Inventory.objects.raw('''
        SELECT inventory.*, product.product_name AS product_name,
                product.slug AS slug,
                variant.variant_name AS variant_name           
                FROM ecommerce_access_inventory AS inventory
                LEFT JOIN ecommerce_access_products AS product
                ON inventory.product_id = product.id
                LEFT JOIN ecommerce_access_productvariant AS variant
                ON inventory.variant_id = variant.id
                WHERE inventory.deleted = false
                AND inventory.product_id = %s 
                ORDER BY inventory.product_id DESC;
        ''',[query])
        return inventory

class CartDA():

    def __init__(self):
        pass

    def get_cart_by_user(self, user_id):
        product_name = Products.objects.filter(id = OuterRef('product_id')).values('product_name')[:1]
        variant_name = ProductVariant.objects.filter(id = OuterRef('variant_id')).values('variant_name')[:1]
        variant_price = ProductVariant.objects.filter(id=OuterRef('variant_id')).values('price')[:1]
        product_media = ProductMedia.objects.filter(product_id = OuterRef('product_id'), media_type = ProductMedia.IMAGE).values('file')[:1]

        return CartReservation.objects.filter(user_id=user_id, status__in=['RESERVED','EXPIRED']
                                              ).annotate(product_name = Subquery(product_name, output_field= CharField()),
                                                         variant_name = Subquery(variant_name, output_field=CharField()),
                                                         price = Subquery(variant_price, output_field=DecimalField()),
                                                         product_media = Subquery(product_media, output_field=CharField())
                                                         ).order_by('reserved_at')
    
    def get_reserved_items(self):
        return CartReservation.objects.filter(status='RESERVED').order_by('reserved_at')
    
    def add_to_cart(self, user_id, data_dict):
        try:
            return CartReservation.objects.create(user_id=user_id, **data_dict)
        except Exception as err:
            return str(err)

    def remove_from_cart(self, user_id, data_dict):
        try:
            variant_id = data_dict.get('variant_id')
            items_deleted, _ = CartReservation.objects.filter(user_id=user_id, variant_id=variant_id).delete()

            if items_deleted > 0:
                return f'{items_deleted} item(s) removed from cart for user {user_id}.'
            else:
                return f'No items found in cart for user {user_id} with variant ID {variant_id}.'

        except Exception as err:
            return str(err)
        
    def remove_with_cart_id(self, cart_id):
        try:
            items_deleted, _ = CartReservation.objects.filter(id=cart_id).delete()

            if items_deleted > 0:
                return f'{items_deleted} item(s) removed from cart .'
            else:
                return f'No items found in cart.'

        except Exception as err:
            return str(err)
        
    def update_item_quantity_in_cart(self, user_id, data_dict):
        try:
            variant_id = data_dict.get('variant_id')
            quantity = int(data_dict.get('quantity', 0))
            item = CartReservation.objects.get(user_id=user_id, variant_id=variant_id, status__in=['RESERVED', 'EXPIRED'])
            quantity += item.quantity
            item.quantity=quantity
            item.save()
            return item

        except Exception as err:
            return str(err)
        
    def get_item_in_cart_by_id(self, user_id, variant_id):
        return get_object_or_404(CartReservation,user_id=user_id, variant_id=variant_id)
    
    def delete_cart_by_user(self, user_id):
        try:
            cart = CartReservation.objects.filter(user_id=user_id)
            items_deleted, _ = cart.delete()

            if items_deleted > 0:
                return f'{items_deleted} item(s) removed from the cart for user {user_id}.'
            else:
                return f'No items found in the cart for user {user_id}.'

        except Exception as err:
            return str(err)
    
    def clear_reservation(self, cart):
        cart.status = 'EXPIRED'
        cart.save()
        InventoryDA().update_inventory_on_reservation_expiry(cart.variant_id, cart.quantity)
        return cart
    
    def get_all_records(self):
        return CartReservation.objects.all()
    
    def get_cart_record_by_cart_id(self, cart_id):
        return CartReservation.objects.get(id=cart_id)
    
    def update_reservation_on_order(self, cart_id):
        try:
            updated = CartReservation.objects.filter(id = cart_id).update(status = 'ORDERED')
            return updated
        except:
            return None
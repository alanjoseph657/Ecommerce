from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum, Count
from django.utils import timezone

from datetime import timedelta

from Ecommerce.dataaccess.ecommerce_access.order_models import Order
from Ecommerce.dataaccess.ecommerce_access.order_models import OrderItem
from Ecommerce.dataaccess.ecommerce_access.order_models import OrderHistory


class OrderDA():

    def __init__(self):
        pass

    def get_all_orders(self):
        return Order.objects.all()
    
    def get_orders_by_user(self, user_id):
        return Order.objects.filter(user_id=user_id).order_by('-created_at')
    
    def get_active_orders(self):
        return Order.objects.filter(status__in=['PENDING','SHIPPED'])
    
    def get_inactvie_orders(self):
        return Order.objects.filter(status__in=['DELIVERED','CANCELLED'])
    
    def get_completed_orders(self):
        return Order.objects.filter(status='DELIVERED')
    
    def get_cancelled_orders(self):
        return Order.objects.filter(status='CANCELLED')
    
    def get_order_details_by_id(self, order_id):
        return get_object_or_404(Order,id=order_id)
    
    def get_orders_by_status(self, status):
        return Order.objects.filter(status=status)
    
    def get_order_status_chart(self):
        order_status_counts = Order.objects.values('status').annotate(count=Count('status'))
        return order_status_counts
    
    def get_orders_by_product(self,product_id):
        order_list = OrderItem.objects.filter(product_id=product_id).order_by('variant_id')
        order_id = order_list.values_list('order',flat=True)
        orders = Order.objects.filter(id__in=order_id)
        return orders
    
    def get_orders_by_date(self, filter_date):
        return Order.objects.filter(created_at=filter_date)
    
    def get_order_items_by_order_id(self, order_id):
        return OrderItem.objects.filter(order_id= order_id).values('variant_id')
    
    def get_all_items_by_order_id(self, order_id):
        return OrderItem.objects.filter(order= order_id)
    
    def create_new_order(self, data_dict):
        try:
            obj = Order.objects.create(**data_dict)
        except Exception as err:
            return str(err)
        return obj
    
    def add_item_to_order(self, data_dict):
        try:
            obj = OrderItem.objects.create(**data_dict)
        except Exception as err:
            return str(err)
        return obj

    def change_order_status(self, order_id, status):
        return Order.objects.filter(id=order_id).update(status=status)
    
    def update_payment(self, order_id, pay_dict):
        return Order.objects.filter(id=order_id).update(**pay_dict)
    
    def cancel_order(self, order_id, note=None):
        order_detail = Order.objects.get(id=order_id)

        if order_detail.payment_status == 'PAID':
            return Order.objects.filter(id=order_id).update(
                status='CANCELLED', 
                note=note, 
                payment_status='REPAYMENT_INITIATED')
        return Order.objects.filter(id=order_id).update(status='CANCELLED', note=note)
    
    def get_order_history_by_user(self, user_id):
        return OrderHistory.objects.filter(user_id=user_id).order_by('-order_id')
    
    def create_order_history(self, data_dict):
        return OrderHistory.objects.create(**data_dict)
    
    def update_order_history(self, order_id, status):
        history =  OrderHistory.objects.filter(order_id = order_id)
        history.update(status=status)
        return history
    
    def clear_order_history_by_user(self, user_id):
        try:
            deleted,_ = OrderHistory.objects.filter(user_id=user_id).delete()
            if deleted == 0:
                raise OrderHistory.DoesNotExist(f'No history found for {user_id}.')
            return deleted
        except Exception as err:
            return str(err)
        
    def filter_order_with_id(self, query, status = None):
        if status:
            return Order.objects.filter(id__icontains= query,status=status).order_by('-created_at')
        else:
            return Order.objects.filter(id__icontains= query).order_by('-created_at')
        
    def get_orders_with_product_and_variant(self, order_id):
        orders = OrderItem.objects.raw('''
            SELECT orderitem.*, product.product_name AS product_name,product.slug AS slug, variant.variant_name AS variant_name
            FROM ecommerce_access_orderitem AS orderitem
            LEFT JOIN ecommerce_access_products AS product
            ON orderitem.product_id = product.id
            LEFT JOIN ecommerce_access_productvariant AS variant
            ON orderitem.variant_id = variant.id
            WHERE orderitem.order = %s
            ''',[order_id]
        )
        return orders
    
    def get_order_items_with_product_media_and_variant(self, order_id):
        orders = OrderItem.objects.raw('''
            SELECT orderitem.*, product.product_name AS product_name,product.slug AS slug, variant.variant_name AS variant_name,
            (SELECT product_media.file 
            FROM ecommerce_access_productmedia AS product_media 
            WHERE product_media.product_id = product.id 
            ORDER BY product_media.id ASC 
            LIMIT 1) AS media_file
            FROM ecommerce_access_orderitem AS orderitem
            LEFT JOIN ecommerce_access_products AS product
            ON orderitem.product_id = product.id
            LEFT JOIN ecommerce_access_productvariant AS variant
            ON orderitem.variant_id = variant.id
            WHERE orderitem.order = %s
            ''',[order_id]
        )
        return orders
    
    def most_ordered_product(self):
        return OrderItem.objects.values('product_id').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').first()

    def product_of_the_month(self):
        today = timezone.now()
        first_day_of_month = today.replace(day=1)
        order_ids = Order.objects.filter(created_at__gte=first_day_of_month).values_list('id', flat=True)
        return OrderItem.objects.filter(order__in=order_ids).values('product_id').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').first()
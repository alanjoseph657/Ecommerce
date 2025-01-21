from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from celery import shared_task

from Ecommerce.dataaccess.ecommerce_access.inventory_da import InventoryDA
from Ecommerce.dataaccess.ecommerce_access.inventory_da import CartDA
from Ecommerce.dataaccess.ecommerce_access.product_da import ProductDA

from Ecommerce import settings

@shared_task
def check_inventory():
    for instance in InventoryDA().get_available_inventory():
        if instance.stock <= instance.reorder_level:
            send_reorder_mail.delay(instance.id)   


@shared_task
def send_reorder_mail(instance_id):
    instance = InventoryDA().get_inventory_by_inventory_id(instance_id)
    product = ProductDA().get_product_details_by_id(instance.product_id)
    variant = ProductDA().get_product_variant_data(instance.variant_id)
    superusers = User.objects.filter(is_superuser=True)
    subject = f'Reorder Alert: {product}'
    message = f'Stock level for product {product} variant {variant} has reached the reorder level of {instance.reorder_level}. Current stock {instance.stock}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = superusers[0].email
    send_mail(subject, message, from_email, [to_email])


@shared_task
def check_cart_expirations():
    now = timezone.now()
    expired_reservations = CartDA().get_all_records().filter(expires_at__lte=now, status='RESERVED')

    for reservation in expired_reservations:
        CartDA().clear_reservation(reservation)


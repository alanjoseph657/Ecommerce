from django.db import models


class Order(models.Model):
    PENDING = 'PENDING'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (PENDING, ' Pending'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    UNPAID = 'UNPAID'
    PAID = 'PAID'
    REPAYMENT_INITIATED = 'REPAYMENT_INITIATED'
    REPAYMENT_COMPLETED = 'REPAYMENT_COMPLETED'
    PAYMENT_STATUS_CHOICES = [
        (UNPAID, 'Unpaid'),
        (PAID, 'Paid'),
        (REPAYMENT_COMPLETED, 'Repayment Completed'),
        (REPAYMENT_INITIATED, 'Repayment Initiated')
    ]

    CASH = 'CASH'
    CARD = 'CARD'
    UPI = 'UPI'
    BANK_TRANSFER = 'BANK_TRANSFER'
    PAYMENT_MODE_CHOICES = [
        (CASH, 'Cash'),
        (CARD, 'Card'),
        (UPI, 'UPI'),
        (BANK_TRANSFER, 'Bank Transfer'),
    ]

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, default=CASH)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES, default=UNPAID)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    shipping_address_id = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         previous_instance = Order.objects.get(pk = self.pk)
    #         if previous_instance:
    #             if self.status != previous_instance.status:
    #                 OrderHistory.objects.create(
    #                     order_id = self.id,
    #                     status = self.status,
    #                     note = self.note,
    #                 )
    #     super().save(*args, **kwargs)   

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField()
    product_id = models.IntegerField()
    variant_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class OrderHistory(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    variant_id = models.IntegerField()
    status = models.CharField(max_length=10)
    change_date = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True, null=True)
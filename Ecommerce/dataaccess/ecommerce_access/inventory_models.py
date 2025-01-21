from django.db import models

from datetime import datetime, timedelta


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    variant_id = models.IntegerField()
    stock = models.IntegerField(blank=True, null=True)
    reorder_level = models.IntegerField(default=1000)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    
    def save(self, *args, **kwargs):
        latest_history = InventoryHistory.objects.filter(
            product_id=self.product_id,
            variant_id=self.variant_id
        ).order_by('-created_at').first()
        
        if latest_history:
            if self.stock != latest_history.new_stock:
                change = self.stock - latest_history.new_stock
                note=f'Inventory updated. Previous stock: {latest_history.new_stock if latest_history else "None"}. New stock: {self.stock}'
        else:
            change = self.stock
            note=f'New stock added. New stock: {self.stock}'

        InventoryHistory.objects.create(
                product_id=self.product_id,
                variant_id=self.variant_id,
                new_stock=self.stock,
                change=change,
                note=note
            )

        super().save(*args, **kwargs)



class InventoryHistory(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    variant_id = models.IntegerField()
    new_stock = models.IntegerField(default=0)
    change = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartReservation(models.Model):
    RESERVED = 'RESERVED'
    EXPIRED = 'EXPIRED'
    ORDERED = 'ORDERED'
    STATUS_CHOICES = [
        (RESERVED,'Reserved'),
        (EXPIRED,'Expired'),
        (ORDERED,'Ordered')
    ]
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    variant_id = models.IntegerField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=RESERVED)
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expires_at = datetime.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)
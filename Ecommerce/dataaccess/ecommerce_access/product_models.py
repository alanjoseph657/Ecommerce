from django.db import models


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='category/', null=True, blank=True)

    def __str__(self):
        return self.category_name
    

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.IntegerField()
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offer = models.TextField(blank=True, null=True)
    inventory = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        if self.inventory is None or self.inventory == '':
            self.is_active = False
        super(Products, self).save(*args, **kwargs)


class ProductVariant(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    variant_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variant_name
    

class ProductMedia(models.Model):
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    MEDIA_CHOICES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    file = models.FileField(upload_to='product_media/',blank=True, null=True) 
    alt_text = models.TextField(blank=True, null=True, default="Image")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

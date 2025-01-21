from django.db import models


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class WishlistItem(models.Model):
    id = models.AutoField(primary_key=True)
    wishlist_id = models.IntegerField()
    product_id = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

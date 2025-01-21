from django.db.models import F, Subquery, OuterRef, CharField, SlugField

from Ecommerce.dataaccess.ecommerce_access.product_models import ProductMedia, Products
from Ecommerce.dataaccess.ecommerce_access.wishlist_models import Wishlist
from Ecommerce.dataaccess.ecommerce_access.wishlist_models import WishlistItem


class WishlistDA():
    
    def __init__(self):
        pass

    def get_wishlist_by_user(self, user_id):
        try:
            user_wishlist = Wishlist.objects.get(user_id=user_id)
        except Wishlist.DoesNotExist:
            user_wishlist = None
        return user_wishlist
    
    def check_wishlist_item(self, wishlist_id, product_id):
        wishlist = WishlistItem.objects.filter(wishlist_id = wishlist_id, product_id=product_id)
        return wishlist
    
    def get_wishlist_items(self, wishlist_id):
        return WishlistItem.objects.filter(wishlist_id=wishlist_id).order_by('-added_at')
    
    def create_wishlist(self, user_id):
        obj = Wishlist(user_id=user_id)
        obj.save()
        return obj
    
    def add_item_to_wishlist(self, wishlist_id, product_id):
        obj = WishlistItem(wishlist_id=wishlist_id, product_id=product_id)
        obj.save()
        return obj
    
    def remove_from_wishlist(self, wishlist_id, item_id):
        try:
            deleted,_ = WishlistItem.objects.filter(wishlist_id=wishlist_id, product_id=item_id).delete()
            if deleted == 0:
                raise WishlistItem.DoesNotExist(f'Item with id {item_id} does not exist in Wishlist.')
        except Exception as err :
            deleted = str(err)
        return deleted
    
    def delete_wishist_by_user(self, user_id):
        try:
            deleted,_ = Wishlist.objects.filter(user_id=user_id).delete()
            if deleted == 0:
                raise Wishlist.DoesNotExist(f'Wishlist for {user_id} does not exist.')
        except Exception as err :
            deleted = str(err)
        return deleted
    
    def get_wishlist_with_product_and_media(self, user_id):
        product_details = Products.objects.filter(id=OuterRef('product_id')).values('product_name', 'slug', 'price', 'is_active', 'inventory')[:1]
        media_file = ProductMedia.objects.filter(product_id=OuterRef('product_id')).order_by('id').values('file')[:1]
        # wishlist_item_subquery = WishlistItem.objects.filter(wishlist_id=OuterRef('id')).values('product_id')[:1]
        wishlist_id = self.get_wishlist_by_user(user_id).id
        if self.get_wishlist_items(wishlist_id):

            return WishlistItem.objects.filter(wishlist_id=wishlist_id).annotate(
                product_name=
                    Subquery(product_details.values('product_name')),
                slug=
                    Subquery(product_details.values('slug')),
                is_active=
                    Subquery(product_details.values('is_active')),
                stock=
                    Subquery(product_details.values('inventory')),
                price=
                    Subquery(product_details.values('price')),
                media_file=Subquery(media_file)
            ).values('id', 'added_at','product_id', 'product_name', 'slug', 'price', 'media_file', 'is_active', 'stock')
        
        else:
            return None
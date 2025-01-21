from django.core.paginator import Paginator

from Ecommerce.dataaccess.ecommerce_access.wishlist_da import WishlistDA
from Ecommerce.dataaccess.ecommerce_access.product_da import ProductDA


class WishlistBL():
    def __init__(self):
        pass

    def get_user_wishlist_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        page = int(request.GET.get('page', 1))

        try:
            wishlist = WishlistDA().get_wishlist_with_product_and_media(user_id).order_by('product_id')
            if wishlist:
                paginator = Paginator(wishlist, 4)
                page_obj = paginator.page(page)
                if page_obj:
                    response['success'] = True
                    response['wishlist'] = page_obj.object_list
                    response['has_next'] = page_obj.has_next()
                    response['has_previous'] = page_obj.has_previous()
                    response['next_page_number'] = page_obj.next_page_number()
                    response['previous_page_number'] = page_obj.previous_page_number()
        except Exception as err:
            response['error'] = "Wishlist not Found"

        return response         

    def add_to_wishlist_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        product_id = request.GET.get('product_id')

        try:
            wishlist = WishlistDA().get_wishlist_by_user(user_id)
            if not wishlist :
                wishlist = WishlistDA().create_wishlist(user_id)
            check_item = WishlistDA().check_wishlist_item(wishlist.id, product_id)
            if not check_item:
                item = WishlistDA().add_item_to_wishlist(wishlist.id, product_id)
                response['msg'] = "Added to wishlist."
            else:
                response['msg'] = "Already added in wishlist."
            response['success'] = True
            
        except Exception as err:
            response['error'] = "Failed to add to wishlist"

        return response

    def remove_from_wishlist_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        product_id = request.GET.get('product_id')
        user_id = request.user.id

        try:
            wishlist = WishlistDA().get_wishlist_by_user(user_id).id
            item = WishlistDA().remove_from_wishlist(wishlist, product_id)
            response['success'] = True
        except Exception as err:
            response['error'] = "Failed to remove item"
        
        return response

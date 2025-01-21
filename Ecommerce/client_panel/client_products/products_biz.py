from django.core.paginator import Paginator

from Ecommerce.dataaccess.ecommerce_access.product_da import ProductDA
from Ecommerce.dataaccess.ecommerce_access.product_da import CategoryDA


class ProductBL():
    def __init__(self):
        pass

    def get_all_products_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        page = int(request.GET.get('page', 1))
        slug = request.GET.get('slug')
        search_query = request.GET.get('search_query')

        try:
            if search_query:
                products = ProductDA().client_search_products(search_query)
            elif slug:
                category_id = CategoryDA().get_category_by_slug(slug).id
                products = ProductDA().get_products_with_category_id_and_image(category_id=category_id)
            else:
                products = ProductDA().get_all_products_with_category_and_image()

            paginator = Paginator(products, 3)
            page_obj = paginator.page(page)

            if page_obj:
                response['success'] = True
                response['products'] = page_obj.object_list
                response['has_next'] = page_obj.has_next()
                response['has_previous'] = page_obj.has_previous()
                response['next_page_number'] = page_obj.next_page_number()
                response['previous_page_number'] = page_obj.previous_page_number()
            else:
                response['msg'] = "No Products Found"
        except Exception as err:
            response['error'] = str(err)
        
        return response
    
    def get_products_by_category_bl(self, slug):
        response = {"error": None, "success": False, "msg": ""}
        category_id = CategoryDA().get_category_by_slug(slug).id

        try:
            products = ProductDA().get_products_by_category(category_id)
            if products:
                response['success'] = True
                response['products'] = products
            else:
                response['msg'] = "No Products Found"

        except Exception as err:
            response['error'] = str(err)
        return response
    
    def get_product_details_bl(self, slug):
        response = {"error": None, "success": False, "msg": ""}
        try:
            product = ProductDA().get_product_details_by_slug(slug)
            variants = ProductDA().get_product_variants(product.id)
            media = ProductDA().get_product_media(product.id)
            category = CategoryDA().get_category_by_id(product.category_id)

            if product:
                response['success'] = True
                response['products'] = product
                response['category'] = category
                response['variants'] = variants
                response['media'] = media
            else:
                response['msg'] = "Cannot fetch product detail"

        except Exception as err:
            response['error'] = str(err)
        return response
    
    def get_related_products_bl(self, slug):
        response = {"error": None, "success": False, "msg": ""}

        try:
            product = ProductDA().get_product_details_by_slug(slug)
            related_products = ProductDA().get_products_with_category_id_and_image(product.category_id)[:5]

            response['success'] = True
            response['related'] = related_products
        except Exception as err:
            response['error'] = str(err)
        
        return response
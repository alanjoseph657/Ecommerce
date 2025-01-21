from django.db.models import Q, Subquery, OuterRef, CharField, Value as V

from Ecommerce.dataaccess.ecommerce_access.product_models import Categories
from Ecommerce.dataaccess.ecommerce_access.product_models import Products
from Ecommerce.dataaccess.ecommerce_access.product_models import ProductMedia
from Ecommerce.dataaccess.ecommerce_access.product_models import ProductVariant


class CategoryDA():
    
    def __init__(self):
        pass

    def get_category_list(self):
        return Categories.objects.order_by('category_name').values_list('id','category_name')
    
    def get_categories(self):
        return Categories.objects.all().order_by('id')
    
    def get_category_by_id(self, category_id):
        try:
            category = Categories.objects.get(id = category_id)
        except Categories.DoesNotExist:
            category = None
        return category
    
    def get_category_by_slug(self, slug):
        try:
            category = Categories.objects.get(slug = slug)
        except Categories.DoesNotExist:
            category = None
        return category
    
    def check_category_name(self, name):
        return Categories.objects.filter(category_name=name).exists()
    
    def create_category(self, data_dict):
        obj = Categories.objects.create(**data_dict)
        return obj

    def update_category(self, category_id, data_dict):
        response = {"success": False, "msg": ""}
        try:
            updated = Categories.objects.filter(id=category_id).update(**data_dict)
            if updated == 0:
                response["msg"] = f"Category with id {category_id} does not exist."
            else:
                response["success"] = True
        except Exception as err:
            response["msg"] = str(err)
        return response

    def delete_category(self, category_id):
        response = {"success": False, "msg": ""}
        try:
            deleted,_ = Categories.objects.filter(id=category_id).delete()
            if deleted == 0:
                response["msg"] = (f'Category with id {category_id} does not exist.')
            else:
                response["success"] = True
        except Exception as err :
            response["msg"] = str(err)
        return response
    

class ProductDA():

    def __init__(self):
        pass

    def get_latest_products(self):
        return Products.objects.order_by('-is_active','-created_at')[:8]
    
    def get_related_products(self, category_id):
        return Products.objects.filter(category_id=category_id, is_active=True).order_by('-created_at')[:5]
    
    def product_search_suggestions(self, query):
        return Products.objects.filter(Q(deleted= False) & (Q(product_name__icontains = query) | Q(id__contains = query)))

    def get_products(self):
        return Products.objects.order_by('-is_active').values('id','product_name','price','offer_price','is_active')
    
    def get_all_products_data(self):
        return Products.objects.order_by('-is_active')
    
    def get_active_products(self):
        return Products.objects.filter(is_active = True)
    
    def get_product_details_by_id(self, product_id):
        try:
            return Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return None
        
    def get_product_details_by_slug(self, slug):
        try:
            return Products.objects.get(slug=slug)
        except Products.DoesNotExist:
            return None
        
    def check_product_name(self, name):
        return Products.objects.filter(product_name=name).exists()
            
    def get_products_filtered(self, filter_dict):
        return Products.objects.filter(Q(**filter_dict)).order_by('-is_active').values('id','product_name','price','offer_price','is_active')
    
    def get_products_by_category(self, category_id, filter_dict=None):
        if filter_dict:
            return Products.objects.filter(Q(**filter_dict) & Q(category_id=category_id,deleted=False)).order_by('-is_active').values(
                 'id',
                 'product_name',
                 'price',
                 'offer_price',
                 'is_active'
                 )
        return Products.objects.filter(category_id=category_id).order_by('-is_active').values(
             'id',
             'product_name',
             'price',
             'offer_price',
             'is_active'
             )
    
    def get_product_variants(self, product_id):
        return ProductVariant.objects.filter(product_id=product_id)
    
    def get_product_variant_data(self, variant_id):
        try:
            return ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return None    
    
    def get_product_media(self, product_id):
        return ProductMedia.objects.filter(product_id=product_id)
    
    def get_product_media_by_id(self, media_id):
        return ProductMedia.objects.get(id=media_id)
    
    def get_product_status(self, product_id):
        return Products.objects.filter(id=product_id).values('id','is_active')

    def update_product_status(self, product_id, status):
        try:
            updated = Products.objects.filter(id=product_id).update(is_active=status)
        except Exception as err:
            return str(err)        
        return updated
    
    def add_new_product(self, data_dict):
        try:
            obj = Products.objects.create(**data_dict)
        except Exception as err:
            return str(err)
        return obj
    
    def add_product_variant(self, product_id, data_dict):
        try:
            obj = ProductVariant.objects.create(product_id=product_id,**data_dict)
        except Exception as err:
            return str(err)
        return obj
    
    def add_product_media(self, product_id, data_dict):
        try:
            obj = ProductMedia.objects.create(product_id=product_id,**data_dict)
        except Exception as err:
            return str(err)
        return obj
    
    def update_product_details(self, product_id, data_dict):
        updated = Products.objects.filter(id=product_id).update(**data_dict)
        return updated
    
    def update_product_variant_data(self, variant_id, data_dict):
        updated = ProductVariant.objects.filter(id=variant_id).update(**data_dict)
        return updated
    
    def delete_product(self, product_id):
        try:
            deleted,_ = Products.objects.filter(id=product_id).update(deleted=True, is_active=False)
            if deleted == 0:
                raise Products.DoesNotExist(f'Product with id {product_id} does not exist.')
        except Exception as err :
                deleted = str(err)
        return deleted
    
    def delete_product_variant(self, variant_id):
        try:
            deleted,_ = ProductVariant.objects.filter(id=variant_id).delete()
            if deleted == 0:
                raise ProductVariant.DoesNotExist(f'Product Variant with id {variant_id} does not exist.')
        except Exception as err :
                deleted = str(err)
        return deleted
    
    def delete_product_variant_by_product(self, product_id):
        try:
            deleted,_ = ProductVariant.objects.filter(product_id=product_id).delete()
            if deleted == 0:
                raise ProductVariant.DoesNotExist(f'Product variant for {product_id} does not exist.')
        except Exception as err :
                deleted = str(err)
        return deleted
    
    def delete_product_media(self, media_id):
        try:
            deleted,_ = ProductMedia.objects.filter(id=media_id).delete()
            if deleted == 0:
                raise ProductMedia.DoesNotExist(f'Product Media with id {media_id} does not exist.')
        except Exception as err :
                deleted = str(err)
        return deleted
    
    def delete_product_media_by_product(self, product_id):
        try:
            deleted,_ = ProductMedia.objects.filter(product_id=product_id).delete()
            if deleted == 0:
                raise ProductMedia.DoesNotExist(f'Product Media for {product_id} does not exist.')
        except Exception as err :
                deleted = str(err)
        return deleted
    
    def get_products_with_category_name(self, category_id=None, search_query=None):
        categories = Categories.objects.filter(id=OuterRef('category_id')).values('category_name')
        products = Products.objects.filter(deleted=False).annotate(category_name=Subquery(categories, output_field=CharField()))
        if category_id:
            if search_query:
                products = products.filter(category_id=category_id,product_name__icontains=search_query)
            else:
                products = products.filter(category_id=category_id)
        elif search_query:
            products = products.filter(product_name__icontains=search_query)
        products = products.order_by('-is_active')
        return products
    
    def get_variants_with_inventory(self, product_id):
        variants = ProductVariant.objects.raw('''
            SELECT variant.*, inventory.stock AS stock
            FROM ecommerce_access_productvariant AS variant
            LEFT JOIN ecommerce_access_inventory AS inventory
            ON variant.inventory_id = inventory.id
            WHERE variant.product_id = %s
            ORDER BY variant.id;
        ''', [product_id])
        return variants
    
    def update_inventory_for_product(self, product_id, inventory):
        try:
            updated = Products.objects.filter(id=product_id).update(inventory=inventory)
        except Exception as err:
            return str(err)        
        return updated
    
    def search_product_using_name_or_id(self, query):
        search_query = '%' + query + '%'
        product = Products.objects.raw('''
        SELECT product.*, category.category_name AS category_name
        FROM ecommerce_access_products AS product
        LEFT JOIN ecommerce_access_categories AS category
        ON product.category_id = category.id
        WHERE product.product_name LIKE %s
        OR product.id LIKE %s
        ORDER BY product.update_at DESC
        ''',[search_query, search_query]
        )
        return product
    
    def search_product_using_name_for_order(self, query):
        return Products.objects.filter(product_name__icontains =query)
    
    def get_variants_with_product(self):
        variants = ProductVariant.objects.raw('''
            SELECT variant.*, products.product_name AS product_name
            FROM ecommerce_access_productvariant AS variant
            LEFT JOIN ecommerce_access_products AS products
            ON variant.product_id = products.id
            ORDER BY variant.id;
        ''')
        return variants
    
    def get_all_variants(self):
        return ProductVariant.objects.all()
        
    def get_latest_products_with_category_and_image(self):
        products = Products.objects.raw(
            '''
            SELECT product.*, 
                category.category_name AS category_name, 
                (SELECT productmedia.file 
                    FROM ecommerce_access_productmedia AS productmedia 
                    WHERE productmedia.product_id = product.id 
                    ORDER BY productmedia.id 
                    LIMIT 1) AS product_media
            FROM ecommerce_access_products AS product
            LEFT JOIN ecommerce_access_categories AS category
            ON product.category_id = category.id
            WHERE product.is_active = True
            ORDER BY product.created_at DESC
            LIMIT 12
            '''
        )

        return products

    def get_all_products_with_category_and_image(self):
        products = Products.objects.raw(
            '''
            SELECT product.*, 
                category.category_name AS category_name, 
                (SELECT productmedia.file 
                    FROM ecommerce_access_productmedia AS productmedia 
                    WHERE productmedia.product_id = product.id 
                    ORDER BY productmedia.id 
                    LIMIT 1) AS product_media
            FROM ecommerce_access_products AS product
            LEFT JOIN ecommerce_access_categories AS category
            ON product.category_id = category.id
            WHERE product.is_active = True
            ORDER BY product.created_at DESC
            '''
        )
        return products
    
    def client_search_products(self, query):
        seacrh_query = '%' + query + '%'
        products = Products.objects.raw(
            '''
            SELECT product.*, 
                category.category_name AS category_name, 
                (SELECT productmedia.file 
                    FROM ecommerce_access_productmedia AS productmedia 
                    WHERE productmedia.product_id = product.id 
                    ORDER BY productmedia.id 
                    LIMIT 1) AS product_media
            FROM ecommerce_access_products AS product
            LEFT JOIN ecommerce_access_categories AS category
            ON product.category_id = category.id
            WHERE product.is_active = True
            AND product.product_name LIKE %s
            ORDER BY product.created_at DESC
            ''',[seacrh_query]
        )
        return products

    
    def get_products_with_category_id_and_image(self, category_id):
        products = Products.objects.raw(
            '''
            SELECT product.*, 
                category.category_name AS category_name, 
                (SELECT productmedia.file 
                    FROM ecommerce_access_productmedia AS productmedia 
                    WHERE productmedia.product_id = product.id 
                    ORDER BY productmedia.id 
                    LIMIT 1) AS product_media
            FROM ecommerce_access_products AS product
            LEFT JOIN ecommerce_access_categories AS category
            ON product.category_id = category.id
            WHERE product.is_active = True
            AND product.category_id = %s
            ORDER BY product.created_at DESC
            ''',[category_id]
        )
        return products
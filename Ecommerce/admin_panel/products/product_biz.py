import os

from django.utils.text import slugify
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum

from Ecommerce.admin_panel.inventory.inventory_biz import InventoryBL
from Ecommerce.common.validations import validate_alphanumeric_with_spaces
from Ecommerce.common.validations import validate_product_name
from Ecommerce.common.validations import validate_price
from Ecommerce.common.validations import validate_image
from Ecommerce.common.validations import validate_video

from Ecommerce.dataaccess.ecommerce_access.product_da import CategoryDA
from Ecommerce.dataaccess.ecommerce_access.product_da import ProductDA
from Ecommerce.dataaccess.ecommerce_access.inventory_da import InventoryDA



class CategoryBL():
    
    def __init__(self):
        pass
    
    def get_category_dropdown(self):
        category = CategoryDA().get_category_list()
        return category

    def create_category(self,request):
        response = {"error": None, "success": False, "msg": ""}
        name = request.POST.get('category_name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not name:
            response['error'] = "Category name is required"
            return response
        
        slug = slugify(name)
        
        if not validate_alphanumeric_with_spaces(name):
            response['error'] = "Name should contain only alphanumeric characters"
            return response

        if CategoryDA().check_category_name(name=name):
            response['error'] = "Category name already exists"
            return response

        data_dict = {
            'category_name' : name.title(),
            'slug' : slug,
            'description' : description,
        }

        if image:
            fs = FileSystemStorage(location='media/category')
            filename = fs.save(image.name, image)
            uploaded_file_url = os.path.join('category', filename)
            data_dict['image'] = uploaded_file_url

        try:
            category = CategoryDA().create_category(data_dict=data_dict)
            response['success'] = True
            response['msg'] = f"Category '{category.category_name}' created successfully."
        
        except Exception as err:
            response['error'] = "Failed to add new category"

        return response            
    
    def list_categories(self, request, item_per_page=10):
        page_number = request.GET.get('page',1)
        response = {"error": None, "success": False, "msg": "", "paginated_categories": None}
        try:
            categories = CategoryDA().get_categories()
            if categories:
                paginator = Paginator(categories, item_per_page)
                try:
                    paginated_categories = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_categories = paginator.page(1)
                except EmptyPage:
                    paginated_categories = paginator.page(paginator.num_pages)
                response["paginated_categories"] = paginated_categories
                response["success"] = True
            else:
                response['error'] = "No category added"
        except Exception as err:
            response['error'] = "No category found"
        return response
    
    def update_category(self, request, slug):
        category_data = CategoryDA().get_category_by_slug(slug)
        category_id = category_data.id
        previous_name = category_data.category_name
        response = {"error": None, "success": False, "msg": ""}
        name = request.POST.get('category_name').title()
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not name:
            response['error'] = "Category name is required"
            return response
        
        slug = slugify(name)
        
        if not validate_alphanumeric_with_spaces(name):
            response['error'] = "Name should contain only alphanumeric characters"
            return response

        if name != previous_name:
            if CategoryDA().check_category_name(name=name):
                response['error'] = "Category name already exists"
                return response

        data_dict = {
            'category_name' : name,
            'slug' : slug,
            'description' : description
        }
        if image:
            fs = FileSystemStorage(location='media/category')
            filename = fs.save(image.name, image)
            uploaded_file_url = os.path.join('category', filename)
            data_dict['image'] = uploaded_file_url
        try:
            category = CategoryDA().update_category(category_id,data_dict)
            response['success'] = True
            response['msg'] = f"Category '{name}' updated successfully."
        
        except Exception as err:
            response['error'] = "Failed to update category"

        return response       
    
    def category_data_by_slug(self, slug):
        response = {"error": None, "success": False, "msg": ""}
        try:
            category = CategoryDA().get_category_by_slug(slug)
            if category:
                return category
            else:
                response['error'] = "Category not found"

        except Exception as err:
            response['error'] = "Category not found"
        return response
    
    def delete_category_by_slug(self, slug):
        response = {"error": None, "success": False, "msg": ""}
        category = CategoryDA().get_category_by_slug(slug)
        category_image = category.image

        if category_image:
            image_path = os.path.join('media', category_image)
            os.remove(image_path)

        check_products = ProductDA().get_products_by_category(category_id=category.id)
        if check_products:
            response['error'] = "Products added under category. Cannot delete category."
        
        else:
            if category:
                deleted = CategoryDA().delete_category(category.id)
                response["success"] = True
                response['msg'] = f"Category deleted successfully."
            else:
                response['error'] = "Category not Found"
        return response


class ProductBL():

    def __init__(self):
        pass

    def list_product_bl(self, request, item_per_page=10):
        page_number = request.GET.get('page',1)  
        category_id = request.GET.get('category_id')
        search_query = request.GET.get('search_query')
        response = {"error": None, "success": False, "msg": "", "paginated_products": None}
        try:
            if search_query:
                if category_id:
                    products = ProductDA().get_products_with_category_name(category_id=category_id, search_query=search_query)
                else:
                    products = ProductDA().get_products_with_category_name(search_query=search_query)
            else:
                if category_id:
                    products = ProductDA().get_products_with_category_name(category_id=category_id)
                else:
                    products = ProductDA().get_products_with_category_name()
                
            if products:
                paginator = Paginator(products, item_per_page)
                try:
                    paginated_products = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_products = paginator.page(1)
                except EmptyPage:
                    paginated_products = paginator.page(paginator.num_pages)
                response["paginated_products"] = paginated_products
                response["success"] = True            
            else:
                response['error'] = "No Product Found"
        except Exception as err:
            response['error'] = "No Product Found"
        return response
    
    def add_product_bl(self,request):
        response = {"error": None, "success": False, "msg": ""}
        category_id = request.POST.get('category')
        name = request.POST.get('product_name').title()
        description = request.POST.get('description')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        media_files = request.FILES.getlist('media_files')

        if not name:
            response['error'] = "Product name is required"
            return response
        
        slug = slugify(name)
        
        if not validate_product_name(name):
            response['error'] = "Name should contain only alphanumeric characters"
            return response
        
        if not validate_price(price):
            response['error'] = "Invalid price"
            return response
        
        if not validate_price(offer_price):
            response['error'] = "Invalid Offer price"
            return response

        if ProductDA().check_product_name(name=name):
            response['error'] = "Product name already exists"
            return response

        product_dict = {
            'category_id' : category_id,
            'product_name' : name,
            'slug' : slug,
            'description' : description,
            'price': price,
            'offer_price' : offer_price
        }

        try:
            product = ProductDA().add_new_product(product_dict)
            if media_files:
                for media_file in media_files:
                    if validate_image(media_file):
                        media_type = 'IMAGE'
                    elif validate_video(media_file):
                        media_type = 'VIDEO'
                    else:
                        response['error'] = f"Unsupported file type: {media_file.content_type}"
                        return response
                    
                    media_data_dict = {
                                'media_type': media_type,
                                'file': media_file,
                                'alt_text': request.POST.get('alt_text', '')  
                            }
                    ProductDA().add_product_media(product.id, media_data_dict)
            response['success'] = True
            response['msg'] = f"Product '{product.product_name}' added successfully."
        
        except Exception as err:
            response['error'] = "Failed to add product"

        return response
    
    def update_product_bl(self, request, product_id):
        product_data = ProductDA().get_product_details_by_id(product_id)
        response = {"error": None, "success": False, "msg": ""}
        category_id = request.POST.get('category')
        name = request.POST.get('product_name').title()
        description = request.POST.get('description')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        previous_name = product_data.product_name
        # media_files = request.FILES.getlist('media_files')
        
        slug = slugify(name)
        
        if not validate_product_name(name):
            response['error'] = "Name should contain only alphanumeric characters"
            return response
        
        if not validate_price(price):
            response['error'] = "Invalid price"
            return response
        
        if not validate_price(offer_price):
            response['error'] = "Invalid Offer price"
            return response

        if name != previous_name:
            if ProductDA().check_product_name(name=name):
                response['error'] = "Product name already exists"
                return response

        product_dict = {
            'category_id' : category_id,
            'product_name' : name,
            'slug' : slug,
            'description' : description,
            'price': price,
            'offer_price' : offer_price
        }

        try:
            ProductDA().update_product_details(product_id, product_dict)
            response['success'] =True
            response['msg'] = "Product details updated successfully"
            response['slug'] = slug
        except Exception as err:
            response['error'] = "Failed to update product"
        
        return response
    
    def update_product_media_bl(self, request, product_id):
        response = {"error": None, "success": False, "msg": ""}
        media_files = request.FILES.getlist('media_files')
        remove_media = request.POST.get('file_ids')
        remove_media = remove_media.split(',')

        try:
            if media_files:
                for media_file in media_files:
                    if validate_image(media_file):
                        media_type = 'IMAGE'
                    elif validate_video(media_file):
                        media_type = 'VIDEO'
                    else:
                        response['error'] = f"Unsupported file type: {media_file.content_type}"
                        return response
                    
                    media_data_dict = {
                                'media_type': media_type,
                                'file': media_file,
                                'alt_text': request.POST.get('alt_text', '')  
                            }
                    ProductDA().add_product_media(product_id, media_data_dict)
            if remove_media != ['']:
                for media_id in remove_media:
                    media = ProductDA().get_product_media_by_id(media_id)
                    if media:
                        file_path = media.file.path
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        ProductDA().delete_product_media(media_id)
            response['success'] = True
            response['msg'] = "Product Media Updated"
        except Exception as err:
            response['error'] = "Failed to update product"
        
        return response
    
    def delete_product_bl(self, slug):
        response = {"error": None, "success": False, "msg": ""}
        product = ProductDA().get_product_details_by_slug(slug)
        product_id = product.id
        product_media = ProductDA().get_product_media(product_id)
        variants = ProductDA().get_product_variants(product_id) 

        try:
            if product_media:
                ProductDA().delete_product_media_by_product(product_id)
            if variants:
                ProductDA().delete_product_variant_by_product(product_id)
            ProductDA().delete_product(product_id)
            InventoryDA().delete_inventory_records_by_product(product_id)
            response['success'] = True
            response['msg'] = "Product deleted"
        except:
            response['error'] = "Failed to delete Product"
        
        return response

    def add_product_variant_bl(self,request,product_id):
        response = {"error": None, "success": False, "msg": ""}
        name = request.POST.get('variant_name')
        price = request.POST.get('price')
        inventory = request.POST.get('inventory')

        if not name:
            response['error'] = "Variant name is required"
            return response

        if not validate_product_name(name):
            response['error'] = "Name should contain only alphanumeric characters"
            return response
        
        if not validate_price(price):
            response['error'] = "Invalid price"
            return response

        variant_dict = {
            'variant_name': name.title(),
            'price' : price
        }
        
        try:
            variant = ProductDA().add_product_variant(product_id, variant_dict)
            if inventory:
                inventory_dict = {
                    'product_id': product_id,
                    'stock': inventory
                }
                inventory_edit = InventoryDA().update_stock_for_variant(variant.id, inventory_dict)
                InventoryBL().save_inventory_history(inventory_edit.id)
                self.auto_update_product_inventory(product_id)
            response['success'] = True
            response['msg'] = f"Variant '{variant.variant_name}' added successfully."

        except Exception as err:
            response['error'] = "Failed to add variant"

        return response

    def get_product_detail(self, slug):
        response = {"error": None, "success": False, "msg": ""}
        try:
            product = ProductDA().get_product_details_by_slug(slug)
            media = ProductDA().get_product_media(product.id)
            variants = ProductDA().get_variants_with_inventory(product.id)
            response['success'] = True
            response['product'] = product
            response['media'] = media
            response['variants'] = variants
        except Exception as err:
            response['error'] = "An error occured"
        return response

    def update_product_variant_bl(self, request):
            response = {"error": None, "success": False, "msg": ""}
            variant_id = request.POST.get('variant_id')
            name = request.POST.get('variant_name')
            price = request.POST.get('price')
            inventory = request.POST.get('inventory')
            product_id = ProductDA().get_product_variant_data(variant_id).product_id

            if not name:
                response['error'] = "Variant name is required"
                return response

            if not validate_product_name(name):
                response['error'] = "Name should contain only alphanumeric characters"
                return response
            
            if not validate_price(price):
                response['error'] = "Invalid price"
                return response
            
            variant_dict = {
                'variant_name': name.title(),
                'price' : price
            }

            inventory_dict = {
                'product_id': product_id,
                'stock': inventory
            }            
            
            try:
                variant = ProductDA().update_product_variant_data(variant_id, variant_dict)
                inventory_edit = InventoryDA().update_stock_for_variant(variant_id, inventory_dict)
                InventoryBL().save_inventory_history(inventory_edit.id)
                self.auto_update_product_inventory(product_id)
                response['success'] = True
                response['msg'] = f"Variant '{name}' updated successfully."
            except Exception as err:
                response['error'] = "Failed to update"
                
            return response
    
    def delete_variant_bl(self, variant_id):
        response = {"error": None, "success": False, "msg": ""}
        variant_data = ProductDA().get_product_variant_data(variant_id)
        try:
            InventoryDA().delete_inventory_record(variant_data.inventory_id)
            ProductDA().delete_product_variant(variant_id)
            self.auto_update_product_inventory(variant_data.product_id)
            response['success'] = True
            response['msg'] = "Variant Deleted"
        except Exception as err:
            response['error'] = "An error occured"
        return response
        
    def auto_update_product_inventory(self, product_id):
        response = {"error": None, "success": False, "msg": ""}
        # try:
        inventory = InventoryDA().get_inventory_by_product(product_id).filter(deleted=False)
        total_stock = inventory.aggregate(total_stock=Sum('stock'))
        ProductDA().update_inventory_for_product(product_id, total_stock['total_stock'])
        response['success'] = True
        response['msg'] = "Inventory updated for product id {product_id}"
        # except Exception as err:
        #     response['error'] = str(err)
        return response

#    unused         
    def search_product_using_name_bl(self, request,query= None, item_per_page=10):
        page_number = request.GET.get('page',1)  
        response = {"error": None, "success": False, "msg": "", "paginated_products": None}
        try:
            products = ProductDA().search_product_using_name_or_id(query)

            if products:
                paginator = Paginator(products, item_per_page)
                try:
                    paginated_products = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_products = paginator.page(1)
                except EmptyPage:
                    paginated_products = paginator.page(paginator.num_pages)
                response["paginated_products"] = paginated_products
                response["success"] = True        
            else:
                response['error'] = "No Product Found"
        except Exception as err:
            response['error'] = "No Product Found"
        return response
    
    def check_status_change(self, request):
        response = {"error": None, "success": False, "msg": "", "paginated_products": None}
        product_id = request.POST.get('product_id')
        if request.POST.get('status').lower() in ['true', '1', 'yes'] :
            product_variant = ProductDA().get_product_variants(product_id)
            product_inventory = ProductDA().get_product_details_by_id(product_id).inventory

            if not product_variant:
                response['error'] = "Add a product variant and inventory"
            
            elif not product_inventory:
                response['error'] = "No inventory"
            
            else:
                try:
                    ProductDA().update_product_status(product_id, status= True)
                    response['success'] = True
                    response['msg'] = "Product Status changed succefully"
                except Exception as err:
                    response['error'] = str(err)
                    
        elif request.POST.get('status').lower() in ['false', '0', 'no']:
            try:
                ProductDA().update_product_status(product_id, status= False)
                response['success'] = True
                response['msg'] = "Product Status changed succefully"
            except Exception as err:
                response['error'] = str(err)

        else:
            response['error'] = "Invalid input"
        
        return response
    
    def product_search_suggestion(self, request):
        query = request.GET.get('q', '')
        if query:
            results = ProductDA().product_search_suggestions(query)
            suggestions = [{'id':result.id , 'name': result.product_name} for result in results]
        else:
            suggestions = []
        return suggestions
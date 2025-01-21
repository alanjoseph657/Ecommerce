from Ecommerce.dataaccess.ecommerce_access.product_da import CategoryDA
from Ecommerce.dataaccess.ecommerce_access.product_da import ProductDA
from Ecommerce.dataaccess.ecommerce_access.order_da import OrderDA
from Ecommerce.dataaccess.ecommerce_access.user_da import ClientMessagesDA
from Ecommerce.common.validations import validate_message_email

class HomepageBL():
    def __init__(self):
        pass

    def get_categories_bl(self):
        response = {"error": None, "success": False, "msg": ""}
        try:
            categories = CategoryDA().get_categories()

            if categories:
                category_list = list(categories.values('id', 'category_name', 'slug', 'image'))
                response['success'] = True
                response['categories'] = category_list
            else:
                response['error'] = True
        except Exception as err:
            response['error'] = str(err)
        return response
    
    def get_latest_products_bl(self):
        response = {"error": None, "success": False, "msg": ""}
        try:
            products = ProductDA().get_latest_products_with_category_and_image()
            if products:
                response['success'] = True
                response['products'] = products
            else:
                response['error'] = "No Products Found"
        except Exception as err:
            response['error'] = str(err)
        
        return response
    
    def get_most_oredered_of_month_bl(self):
        response = {"error": None, "success": False, "msg": ""}
        try:    
            product_id = OrderDA().product_of_the_month()
            product_details = ProductDA().get_product_details_by_id(product_id['product_id'])
            product_media = ProductDA().get_product_media(product_id['product_id']).first()
            response['success'] = True
            response['product_details'] = product_details
            response['product_media'] = product_media
        except Exception as err:
            response['error'] = str(err)

        return response
    
    def add_new_client_message_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not validate_message_email(email):
            response['error'] = "Invalid email"
            return response

        try:
            data_dict = {
                'name': name,
                'email': email,
                'message': message
            }

            add_message = ClientMessagesDA().add_new_client_message(data_dict)
            if add_message:
                response['success'] = True
                response['msg'] = "Message sent. Please wait for your reply"
            else:
                response['error'] = "Failed to send message"
        except Exception as err:
            exception = str(err)
            response['error'] = "Failed to send message"
        return response

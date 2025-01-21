from django.contrib.auth.models import User

from Ecommerce.common.utilities import generate_otp, send_otp_email
from Ecommerce.common.validations import validate_email, validate_username
from Ecommerce.dataaccess.ecommerce_access.user_da import AddressDA
from Ecommerce.dataaccess.ecommerce_access.user_da import UserDA


class ProfileBL():
    def __init__(self):
        pass

    def get_user_profile_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id

        try:
            user = UserDA().get_user_by_id(user_id)
            user_profile = UserDA().get_user_profile_by_user_id(user_id)
            response['success'] = True
            response['user'] = user
            response['profile'] = user_profile
        except Exception as err:
            response['error'] = "User not Found"
        return response
    
    def update_user_profile_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        new_username = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('phone_number')

        try:
            username = UserDA().get_user_by_id(user_id).username

            if new_username != username:
                username_validate = validate_username(username)
                if username_validate != True:
                    response['error'] = username_validate
                    return response
            
            user_dict = {
                'username':username,
                'email':email
            }
            
            UserDA().update_user_data(user_id, user_dict)
            
            profile = UserDA().get_user_profile_by_user_id(user_id)
            profile_dict = {
                    'phone_number': contact,
                }
            if profile:
                UserDA().update_user_profile(user_id, profile_dict)
            else:
                UserDA().create_user_profile(user_id, profile_dict)

            response['success'] = True
            response['msg'] = "Profile Updated successfully"
        except Exception as err:
            response['error'] = "Failed to update profile"
        
        return response
    
    def generate_otp_for_email_change(self, request):
        response = {"error": None, "success": False, "msg": ""}
        email = request.POST.get('email')
        user_id = request.user.id

        validated_email = validate_email(email)
        if not validated_email:
            response['error'] = "Email invalid or already exists"
            return response
        
        try:
            otp = generate_otp()
            UserDA().add_otp_for_user_id(user_id, otp)
            send_otp_email(email=email, otp= otp)
            response['success'] = True
            response['msg'] = "Otp has been sent to the mail id successfully"
            response['otp'] = otp
        except:
            response['error'] = "Failed to verify email"
        
        return response
    
    def verify_otp_for_email_change(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        otp = request.POST.get('otp')

        try:
            check_otp = UserDA().get_otp_for_user_id(user_id)
            if int(otp) == check_otp.otp:
                UserDA().delete_otp_record(user_id)
                response['success'] = True
                response['msg'] = "otp verified"
            else:
                response['error'] = "otp verification failed"
        except:
            response['error'] = "otp verification failed"
        return response
    

class AddressBL():
    def __init__(self):
        pass

    def add_edit_address_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        address_id = request.POST.get('address_id')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        name = request.POST.get('name')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        alt_number = request.POST.get('contact')
        postal_code = request.POST.get('postal_code')
        is_default = request.POST.get('default')

        try:
            data_dict={
                'name': name,
                'address_line1': address1,
                'address_line2': address2,
                'city' : city,
                'state' : state,
                'country' : country,
                'alt_number' : alt_number,
                'postal_code' : postal_code
            }

            check_address = AddressDA().get_addresses_by_user(user_id)

            if (not check_address) or (is_default == 'on') :
                data_dict['is_default'] = True

            if address_id:
                if is_default == 'on':
                    AddressDA().set_as_default_address(user_id, address_id)
                AddressDA().edit_address(address_id , data_dict)
            
            else:
                address = AddressDA().add_new_address(user_id, data_dict)
                if is_default == 'on':
                    AddressDA().set_as_default_address(user_id, address.id)

            response['success'] = True
            response['msg'] = "Address updated"

        except Exception as err:
            response['error'] = "Failed to update address"

        return response
    
    def get_address_for_user_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id

        try:
            addresses = AddressDA().get_addresses_by_user(user_id)
            response['success'] = True
            response['addresses'] = addresses
        except Exception as err:
            response['error'] = "No Records Found"
        return response

    def get_shipping_address_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id

        try:
            addresses = AddressDA().get_addresses_by_user(user_id)
            shipping_address = addresses.filter(is_default = True)
            for data in addresses:
                if data.used_for_last_order:
                    shipping_address = data
            
            response['success'] = True
            response['addresses'] = addresses
            response['shipping_address'] = shipping_address
        except Exception as err:
            response['error'] = "Error fetching address"
        
        return response
    
    def get_address_values_for_cart_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        address_id = request.GET.get('address_id')

        try:
            addresses = AddressDA().get_address_values_by_id(address_id)
            
            response['success'] = True
            response['new_address'] = addresses
        except Exception as err:
            response['error'] = "Error fetching address"
        
        return response
    
    def delete_address_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        address_id = request.GET.get('address_id')
        user_id = request.user.id

        try:
            address = AddressDA().get_address_by_id(address_id)
            if address.is_default:
                new_default = AddressDA().get_addresses_by_user(user_id).filter(is_default=False).first()
                AddressDA().set_as_default_address(user_id, new_default.id)
            AddressDA().delete_address(address_id)
            response['success'] = True
            response['msg'] = "Address deleted succesfully"
        except Exception as err:
            response['error'] = "Failed to delete address"
        return response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

from Ecommerce.dataaccess.ecommerce_access.user_models import UserProfile
from Ecommerce.dataaccess.ecommerce_access.user_models import ClientReport
from Ecommerce.dataaccess.ecommerce_access.user_models import ShippingAddress
from Ecommerce.dataaccess.ecommerce_access.user_models import VerificationOtp
from Ecommerce.dataaccess.ecommerce_access.user_models import ClientMessages


class UserDA():

    def __init__(self):
        pass
    
    def get_otp_for_user_id(self, user_id):
        return VerificationOtp.objects.get(user_id=user_id)
    
    def get_otp_for_email(self, email):
        return VerificationOtp.objects.filter(email=email).order_by('-id').first()
    
    def add_otp_for_user_id(self, user_id, otp):
        try:
            return VerificationOtp.objects.update_or_create(user_id=user_id, defaults={'otp':otp})
        except Exception as err:
            return str(err)
    
    def add_otp_for_email(self, email, otp):
        try:
            return VerificationOtp.objects.update_or_create(email=email, defaults={'otp':otp})
        except Exception as err:
            return str(err)
        
    def delete_otp_record_email(self, email):
        try:
            deleted,_ = VerificationOtp.objects.filter(email=email).delete()
            if deleted == 0:
                raise VerificationOtp.DoesNotExist(f'No record found.')
            return deleted
        except Exception as err:
            return str(err)
  
    def delete_otp_record(self, user_id):
        try:
            deleted,_ = VerificationOtp.objects.filter(user_id=user_id).delete()
            if deleted == 0:
                raise VerificationOtp.DoesNotExist(f'No record found.')
            return deleted
        except Exception as err:
            return str(err)
    
    def get_all_users(self):
        return User.objects.all().order_by('id')
    
    def get_user_by_username(self, name):
        try:
            return User.objects.get(username=name)
        except User.DoesNotExist:
            return None
    
    def check_valid_user_id_password(self, user_id, password):
        return User.objects.filter(id=user_id, password=password).exists()
    
    def get_all_admin(self):
        return User.objects.filter(is_staff=True).order_by('id')
    
    def get_all_clients(self):
        return User.objects.filter(is_staff=False).order_by('id')
    
    def get_user_by_id(self, user_id):  
        return User.objects.get(id=user_id)
    
    def is_admin(self, user_id):
        user = self.get_user_by_id(user_id)
        if isinstance(user, User):
            return user.is_staff
        return False
    
    def get_username_by_email(self, email):
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            username = None
        return username
    
    def get_user_by_email(self, email):
        return User.objects.get(email=email)
    
    def get_user_email(self, user_id):
        return User.objects.get(id=user_id).email
    
    def get_all_user_email(self):
        return User.objects.values_list('id','email')
    
    def get_user_by_filter(self, filter_dict):
        return User.objects.filter(Q(**filter_dict))
    
    def get_all_user_profile(self):
        return UserProfile.objects.all()
    
    def get_user_profile_by_id(self, profile_id):
        return get_object_or_404(UserProfile,id=profile_id)
    
    def get_user_profile_by_user_id(self, user_id):
        try:
            return UserProfile.objects.get(user_id=user_id)
        except:
            return None
    
    def update_user_profile(self, user_id, data_dict):
        try:
            updated = UserProfile.objects.filter(user_id=user_id).update(**data_dict)
            if updated == 0:
                raise UserProfile.DoesNotExist(f'UserProfile with id {user_id} does not exist.')
            return updated
        except Exception as err:
            return str(err)
        
    def update_user_data(self, user_id, data_dict):
        try:
            user = get_object_or_404(User, id=user_id)
            for field, value in data_dict.items():
                setattr(user, field, value)
            user.save()
            return user
        except Exception as err:
            return str(err)
        
    def update_user_password(self, user_id, new_password):
        try:
            user = get_object_or_404(User, id=user_id)
            user.set_password(new_password)
            user.save()
            return user
        except Exception as err:
            return str(err)
    
    def delete_user(self, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return f'User with id {user_id} has been deleted.'
        except Exception as err:
            return str(err)
    
    def create_user(self, username, email, password):
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return user
        except Exception as err:
            return str(err)

    def create_admin_user(self, username, email, password):
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            return user
        except Exception as err:
            return str(err)
        
    def create_user_profile(self, user_id, data_dict):
        try:
            profile = UserProfile.objects.create(user_id=user_id, **data_dict)
        except Exception as err:
            return str(err)
        return profile
    

class AddressDA():

    def __init__(self):
        pass

    def get_addresses_by_user(self, user_id):
        return ShippingAddress.objects.filter(user_id=user_id).order_by('created_at')
    
    def get_address_values_by_id(self, address_id):
        address = ShippingAddress.objects.filter(id=address_id)
        return list(address.values(
            'id', 'name', 'address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code', 'alt_number'))
    
    def get_address_by_id(self, address_id):
        return get_object_or_404(ShippingAddress, id=address_id)
    
    def get_default_address(self, user_id):
        return get_object_or_404(ShippingAddress, user_id=user_id, is_default=True)
    
    def last_order_address(self, user_id):
        return get_object_or_404(ShippingAddress, user_id=user_id, used_for_last_order=True)
    
    def set_as_last_order_address(self, address_id):
        try:
            updated = ShippingAddress.objects.filter(id=address_id).update(used_for_last_order=True)
            if updated == 0:
                raise ShippingAddress.DoesNotExist(f'Address with id {address_id} does not exist.')
            return updated
        except Exception as err:
            return str(err)

    def remove_last_order_address(self, user_id):
        try:
            address = ShippingAddress.objects.filter(user_id=user_id, used_for_last_order=True)
            address.update(used_for_last_order=False)
            if address == 0:
                raise ShippingAddress.DoesNotExist(f'No address set as last order address.')
            return address
        except Exception as err:
            return str(err)

    def set_as_default_address(self, user_id, address_id):
        try:
            ShippingAddress.objects.filter(user_id=user_id).update(is_default=False)
            new_default = ShippingAddress.objects.filter(id=address_id).update(is_default=True)
            if new_default == 0:
                raise ShippingAddress.DoesNotExist(f'No address found for id {address_id}.')
            return new_default
        except Exception as err:
            return str(err)
        
    def add_new_address(self, user_id, data_dict):
        return ShippingAddress.objects.create(user_id=user_id, **data_dict)
    
    def edit_address(self, address_id, data_dict):
        try:
            updated = ShippingAddress.objects.filter(id=address_id).update(**data_dict)
            if updated == 0:
                raise ShippingAddress.DoesNotExist(f'No address found for id {address_id}.')
            return updated
        except Exception as err:
            return str(err)
        
    def delete_address(self, address_id):
        address = get_object_or_404(ShippingAddress, id=address_id)
        address.delete()
        return f'Address {address_id} has been deleted successfully.'

    def delete_address_by_user_id(self, user_id):
        try:
            address,_ = ShippingAddress.objects.filter(user_id=user_id).delete()
            if address == 0:
                raise ShippingAddress.DoesNotExist(f'No address found for user {user_id}.')
            return address
        except Exception as err:
            return str(err)
        

class ClientReportDA():

    def __init__(self):
        pass

    def get_all_reports(self):
        return ClientReport.objects.all().order_by('-created_at')
    
    def report_search_suggestions(self, query):
        return ClientReport.objects.filter(report_name__icontains=query)
    
    def get_reports_by_user_id(self, user_id):
        return ClientReport.objects.filter(user_id=user_id).order_by('-created_at')
    
    def get_report_by_id(self, report_id):
        return get_object_or_404(ClientReport, id=report_id)
    
    def get_report_by_filter(self, filter_dict):
        return ClientReport.objects.filter(Q(**filter_dict))
    
    def create_new_report(self, data_dict):
        try:
            return ClientReport.objects.create(**data_dict)
        except Exception as err:
            return str(err)
        
    def update_report(self, report_id, data_dict):
        try:
            updated = ClientReport.objects.filter(id=report_id).update(**data_dict)
            if updated == 0:
                raise ClientReport.DoesNotExist(f'No report found for {report_id}.')
            return updated
        except Exception as err:
            return str(err)
    
    def delete_report(self, report_id):
        try:
            report,_ = ClientReport.objects.filter(id=report_id).delete()
            if report == 0:
                raise ClientReport.DoesNotExist(f'No report found for {report_id}.')
            return report
        except Exception as err:
            return str(err)
    
    def client_report_with_client_name_and_admin(self, query=None, date=None):
        sql_query = '''
        SELECT report.*, user.username as client_name, admin_user.username as admin
        FROM ecommerce_access_clientreport AS report
        LEFT JOIN auth_user as user
        ON report.user_id = user.id
        LEFT JOIN auth_user as admin_user   
        ON report.created_by = admin_user.id
        '''
        params = []
        
        if query:
            search_query = '%' + query + '%'
            sql_query += 'WHERE report.report_name LIKE %s '
            params.append(search_query)
        
        if date:
            if query:
                sql_query += 'AND DATE(report.created_at) = %s '
            else:
                sql_query += 'WHERE DATE(report.created_at) = %s '
            params.append(date)
            
        sql_query += 'ORDER BY report.update_at DESC'
        
        reports = ClientReport.objects.raw(sql_query, params)
        return reports
    
    def client_report_with_client_name_and_admin_by_admin(self, admin_id, search_date=None):
        sql_query ='''
            SELECT report.*,user.username as client_name , admin_user.username as admin
            FROM ecommerce_access_clientreport AS report
            LEFT JOIN auth_user as user
            ON report.user_id = user.id
            LEFT JOIN auth_user as admin_user
            ON report.created_by = admin_user.id
            WHERE report.created_by = %s
            '''
        
        params = [admin_id]
        
        if search_date:
            sql_query += 'AND DATE(report.created_at) = %s'
            params.append(search_date)
        
        sql_query += 'ORDER BY report.update_at DESC'

        reports = ClientReport.objects.raw(sql_query, params)
        return reports
    
    def client_report_for_dashboard(self):
        reports = ClientReport.objects.raw('''
            SELECT report.*,user.username as client_name , admin_user.username as admin
            FROM ecommerce_access_clientreport AS report
            LEFT JOIN auth_user as user
            ON report.user_id = user.id
            LEFT JOIN auth_user as admin_user
            ON report.created_by = admin_user.id
            ORDER BY report.update_at DESC
            LIMIT 5;
            ''')
        return reports
    
    # def client_report_with_client_name_and_admin(self, query=None, created_at_date=None):
    # sql_query = '''
    #     SELECT report.*, user.username as client_name, admin_user.username as admin
    #     FROM ecommerce_access_clientreport AS report
    #     LEFT JOIN auth_user as user
    #     ON report.user_id = user.id
    #     LEFT JOIN auth_user as admin_user
    #     ON report.created_by = admin_user.id
    # '''
    # params = []
    # conditions = []

    # if query:
    #     search_query = '%' + query + '%'
    #     conditions.append('report.report_name LIKE %s')
    #     params.append(search_query)
        
    # if created_at_date:
    #     conditions.append('report.created_at = %s')
    #     params.append(created_at_date)

    # if conditions:
    #     sql_query += 'WHERE ' + ' AND '.join(conditions)
        
    # sql_query += ' ORDER BY report.update_at DESC'
    
    # reports = ClientReport.objects.raw(sql_query, params)
    # return reports


class ClientMessagesDA():
    def __init__(self):
        pass

    def add_new_client_message(self, data_dict):
        try:
            created = ClientMessages.objects.create(**data_dict)
        except:
            created = None
        return created

    def get_all_messages(self):
        return ClientMessages.objects.all()
    
    def get_message_detail_by_id(self, message_id):
        try:
            return ClientMessages.objects.get(id= message_id)
        except:
            return None
        
    def update_message_details(self, message_id, data_dict):
        try:
            updated = ClientMessages.objects.filter(id=message_id).update(**data_dict)
        except:
            updated = None
        return updated
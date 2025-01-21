from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from Ecommerce.common.forms import CaptchaForm
from Ecommerce.dataaccess.ecommerce_access.user_da import UserDA
from Ecommerce.dataaccess.ecommerce_access.user_da import ClientReportDA
from Ecommerce.common.validations import validate_username
from Ecommerce.common.validations import validate_email
from Ecommerce.common.validations import validate_password
from Ecommerce.common.utilities import generate_otp, send_otp_email


class UserBL():
    def __init__(self):
        pass

    def check_client_exist_bl(self, name):
        response = {"error": None, "success": False, "msg": ""}
        try:
            client = UserDA().get_user_by_username(name)
            if client:
                response['success'] = True
            else:
                response['error'] = "Invalid Client Name"
        except Exception as err:
            response['error'] = str(err)

        return response

    def sign_up_admin_user(self, request):
        response = {"error": None, "success": False, "msg": ""}
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        captcha_form = CaptchaForm(request.POST)

        if not captcha_form.is_valid():
            response['error'] = "Captcha Verification failed"
            return response

        if password != password2:
            response['error'] = "Password confirmation failed"
            return response

        username_validate = validate_username(username)
        if username_validate != True:
            response['error'] = username_validate
            return response
        
        email_validate = validate_email(email)
        if email_validate != True:
            response['error'] = email_validate
            return response
            
        password_validate = validate_password(password)
        if password_validate != True:
            response['error'] = password_validate
            return response
        
        try:
            UserDA().create_admin_user(username, email, password)
            response['success'] = True
            response['msg'] = "User Created successfully"
        except Exception as err:
            response['error'] = "Sign Up Failed"

        return response

    def generate_otp_for_sign_up(self, request):
        response = {"error": None, "success": False, "msg": ""}
        email = request.POST.get('email')

        validated_email = validate_email(email)
        if not validated_email:
            response['error'] = "Email invalid or already exists"
            return response
        
        try:
            otp = generate_otp()
            UserDA().add_otp_for_email(email, otp)
            send_otp_email(email=email, otp= otp)
            response['success'] = True
            response['msg'] = "Otp has been sent to the mail id successfully"
            response['otp'] = otp
        except:
            response['error'] = "Failed to verify email"
        
        return response
    
    def verify_sign_up_otp_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        print("verify",email,otp)

        try:
            check_otp = UserDA().get_otp_for_email(email)
            if int(otp) == check_otp.otp:
                UserDA().delete_otp_record_email(email)
                response['success'] = True
                response['msg'] = "otp verified"
            else:
                response['error'] = "otp verification failed"
        except:
            response['error'] = "otp verification failed"
        return response

    def login_admin_user(self, request):
        response = {"error": None, "success": False, "msg": ""}
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            response['error'] = "Invalid username or email"
            return response

        if '@' in username:
            username = UserDA().get_username_by_email(username)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                response['success'] = True
                response['msg'] = "Login Success"
            else:
                response['error'] = "You donot have permission to access this page"
        else:
            response['error'] = "Invalid username or password"
        
        return response
    
    def logout_admin_user(self, request):
        response = {"error": None, "success": False, "msg": ""}
        try:
            logout(request)
            response['success'] = True
        except Exception as err:
            response['error'] = "Logout Failed"
        return response
    
    def reset_admin_password(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        username = UserDA().get_user_by_id(user_id).username
        current_password = request.POST.get('current_password')        
        new_password = request.POST.get('new_password')        
        confirm_password = request.POST.get('confirm_password') 

        if new_password != confirm_password:
            response['error'] = "New password confirmation failed"
            return response
        
        password_validate = validate_password(new_password)
        if not password_validate:
            response['error'] = password_validate
            return response
        
        user = authenticate(request, username=username, password=current_password)
        if user is not None:
            try:
                UserDA().update_user_password(user_id, new_password)
                response['success'] = True
                response['msg'] = "Password reset successfully"
            
            except Exception as err:
                response['error'] = "password reset failed"
            
        else:
            response['error'] = "Invalid Current Password"
        
        return response
    
    def reset_forgot_admin_password_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        username = request.GET.get('username')
        user_id = UserDA().get_user_by_username(username).id
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            response['error'] = "New password confirmation failed"
            return response
        
        password_validate = validate_password(password)
        if not password_validate:
            response['error'] = password_validate
            return response
        
        try:
            UserDA().update_user_password(user_id, password)
            response['success'] = True
            response['msg'] = "Password reset successfully"
        
        except Exception as err:
                response['error'] = "Password reset failed"

        return response
        
    def send_otp_mail_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        username = request.GET.get('username')

        if not username:
            response['error'] = "Invalid username or email"
            return response
        
        if '@' in username:
            username = UserDA().get_username_by_email(username)
        else:
            username = UserDA().get_user_by_username(username)
        
        email = username.email

        try:
            otp = generate_otp()
            UserDA().add_otp_for_user_id(username.id, otp)
            send_otp_email(email=email, otp= otp)
            response['success'] = True
            response['msg'] = "Otp has been sent to the registered mail id successfully"
            response['otp'] = otp
        except Exception as err:
            response['error'] = "An error occured"
        return response

    def verify_otp_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        check = request.POST.get('otp')
        username = request.GET.get('username')
        user_id = UserDA().get_user_by_username(username).id
        otp = UserDA().get_otp_for_user_id(user_id)

        if int(check) == int(otp.otp):
            UserDA().delete_otp_record(user_id)
            response['success'] = True
            response['msg'] = "otp verified"
        
        else:
            response['error'] = "otp verification failed"

        return response
    
    def delete_account_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        try:
            UserDA().delete_user(user_id)
            response['success'] = True
            response['msg'] = "Account Deleted"
        except Exception as err:
            response['error'] = "Failed to delete account"
        return response
    

class ClientReportBL():
    def __init__(self):
        pass

    def list_all_client_report_bl(self, request, item_per_page=10):
        page_number = request.GET.get('page',1)  
        response = {"error": None, "success": False, "msg": ""}
        search_date = request.GET.get('search_date')
        query = request.GET.get('search_report')

        try:
            if query:
                if search_date:
                    reports = ClientReportDA().client_report_with_client_name_and_admin(query, date=search_date)
                else:
                    reports = ClientReportDA().client_report_with_client_name_and_admin(query)

            else:
                if search_date:
                    reports = ClientReportDA().client_report_with_client_name_and_admin(date=search_date)
                else:
                    reports = ClientReportDA().client_report_with_client_name_and_admin()
                    
            if reports:
                paginator = Paginator(reports, item_per_page)
                try:
                    paginated_reports = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_reports = paginator.page(1)
                except EmptyPage:
                    paginated_reports = paginator.page(paginator.num_pages)
            response["success"] = True
            response['reports'] = paginated_reports
        except Exception as err:
            response['error'] = "No Reports Found"
        return response
    
    def list_reports_by_date_bl(self, request, item_per_page=10 , search_date=None):
        page_number = request.POST.get('page_number', 1)
        response = {"error": None, "success": False, "msg": ""}
        if (not search_date) and ('search_date' in request.session):
            search_date = request.session['search_date']
        try:
            if search_date:
                reports = ClientReportDA().client_report_with_client_name_and_admin(date=search_date)
            else:
                reports = ClientReportDA().client_report_with_client_name_and_admin()
            
            response["success"] = True
            response['reports'] = reports
        except Exception as err:
            response['error'] = str(err)
        return response
        
    def create_report_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}

        report_name = request.POST.get('report_name')
        client = request.POST.get('client')
        report_data = request.POST.get('report_data')
        created_by = request.user.id
        user_id = UserDA().get_user_by_username(client).id

        if not user_id:
            response['error'] = "Invalid Client"
            return response
        
        data_dict = {
            'user_id': user_id,
            'report_name' : report_name,
            'report_data' : report_data,
            'created_by' : created_by
        }

        try:
            report = ClientReportDA().create_new_report(data_dict)
            response['success'] = True
            response['msg'] = "New Report created"
        except Exception as err:
            response['error'] = "Failed to create report"

        return response
    
    def report_detail_bl(self, report_id):
        response = {"error": None, "success": False, "msg": ""}

        try:
            report = ClientReportDA().get_report_by_id(report_id)
            client_name = UserDA().get_user_by_id(report.user_id).username
            admin = UserDA().get_user_by_id(report.created_by).username
            if report:
                response['success'] = True
                response['report'] = report
                response['client_name'] = client_name
                response['admin'] = admin
            else:
                response['error'] = "Report Not found"
        except Exception as err:
            response['error'] = "Rrport Not Found"
        
        return response
    
    def report_edit_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        report_id = request.POST.get('report_id')
        report_name = request.POST.get('report_name')
        client = request.POST.get('client')
        report_data = request.POST.get('report_data')
        user_id = UserDA().get_user_by_username(client).id

        if not user_id:
            response['error'] = "Invalid Client"
            return response
        
        data_dict = {
            'user_id': user_id,
            'report_name' : report_name,
            'report_data' : report_data,
        }

        try:
            report = ClientReportDA().update_report(report_id, data_dict)
            response['success'] = True
            response['msg'] = "Report updated succefully"

        except Exception as err:
            response['error'] = str(err)
        
        return response
    
    def list_all_client_report_by_admin_bl(self, request, item_per_page=10):
        page_number = request.GET.get('page',1)  
        admin_id = request.user.id
        search_date = request.GET.get('search_date')
        response = {"error": None, "success": False, "msg": ""}
        try:
            if search_date:
                reports = ClientReportDA().client_report_with_client_name_and_admin_by_admin(admin_id,search_date)
            else:
                reports = ClientReportDA().client_report_with_client_name_and_admin_by_admin(admin_id)
            
            if reports:
                paginator = Paginator(reports, item_per_page)
                try:
                    paginated_reports = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_reports = paginator.page(1)
                except EmptyPage:
                    paginated_reports = paginator.page(paginator.num_pages)
            response["success"] = True
            response['reports'] = paginated_reports
        except Exception as err:
            response['error'] = "No Reports Found"
        return response
    
    def report_search_suggestions_bl(self, request):
        query = request.GET.get('q', '')
        if query:
            results = ClientReportDA().report_search_suggestions(query)
            suggestions = [{'id':result.id, 'name':result.report_name} for result in results]
        else:
            suggestions =[]
        return suggestions
    
    def list_all_client_report_by_name_bl(self, request, item_per_page=10, date=None):
        page_number = request.GET.get('page',1) 
        query = request.GET.get('search_report')
        response = {"error": None, "success": False, "msg": ""}
        
        try:
            if query:
                if date:
                    reports = ClientReportDA().client_report_with_client_name_and_admin(query, date=date)
                reports = ClientReportDA().client_report_with_client_name_and_admin(query)

            if reports:
                paginator = Paginator(reports, item_per_page)
                try:
                    paginated_reports = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_reports = paginator.page(1)
                except EmptyPage:
                    paginated_reports = paginator.page(paginator.num_pages)
            response["success"] = True
            response['reports'] = paginated_reports
        except Exception as err:
            response['error'] = "No Reports Found"
        return response
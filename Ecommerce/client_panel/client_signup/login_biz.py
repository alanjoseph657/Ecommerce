from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from Ecommerce.common.forms import CaptchaForm
from Ecommerce.common.validations import validate_username
from Ecommerce.common.validations import validate_email
from Ecommerce.common.validations import validate_password
from Ecommerce.common.utilities import generate_otp, send_otp_email
from Ecommerce.dataaccess.ecommerce_access.user_da import UserDA


class UserBL():
    def __init__(self):
        pass

    def login_user_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        username = request.POST.get('name')
        password = request.POST.get('password')

        if not username:
            response['error'] = "Invalid username or email"
            return response
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response['success'] = True
            response['msg'] = "Login Success"
        else:
            response['error'] = "Invalid username or password"
        
        return response
    
    def logout_user_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        try:
            logout(request)
            response['success'] = True
        except Exception as err:
            response['error'] = str(err)
        return response
    
    def sign_up_user_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        username = request.POST.get('name')
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
            UserDA().create_user(username, email, password)
            response['success'] = True
            response['msg'] = "User Created successfully"
        except Exception as err:
            response['error'] = str(err)

        print(response)

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
            response['email'] = email
        except Exception as err:
            response['error'] = str(err)
        return response
    
    def verify_sent_otp_password(self, request):
        response = {"error": None, "success": False, "msg": ""}
        email = request.GET.get('email')
        otp = request.GET.get('otp')

        try:
            user_id = UserDA().get_user_by_email(email).id
            check_otp = UserDA().get_otp_for_user_id(user_id)
            if int(otp) == check_otp.otp:
                UserDA().delete_otp_record_email(email)
                response['success'] = True
                response['msg'] = "otp verified"
            else:
                response['error'] = "otp verification failed"
        except:
            response['error'] = "otp verification failed"
        return response
    
    def reset_forgot_password_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        username = request.POST.get('email')
        user_id = UserDA().get_user_by_email(username).id
        print(user_id)
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
                response['error'] = str(err)

        return response
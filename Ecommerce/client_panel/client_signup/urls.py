from django.urls import path

from Ecommerce.client_panel.client_signup.views import login_page
from Ecommerce.client_panel.client_signup.views import logout_user_view
from Ecommerce.client_panel.client_signup.views import sign_up_user
from Ecommerce.client_panel.client_signup.views import verify_sign_up_email
from Ecommerce.client_panel.client_signup.views import verify_sign_up_otp
from Ecommerce.client_panel.client_signup.views import forgot_password_user
from Ecommerce.client_panel.client_signup.views import send_otp_for_password_view
from Ecommerce.client_panel.client_signup.views import forgot_password_reset_view

urlpatterns = [
    path('login/',login_page, name="login"),
    path('logout_user/',logout_user_view, name="logout_user"),
    path('sign_up/',sign_up_user, name="sign_up"),
    path('verify_user_sign_up_email/',verify_sign_up_email, name="verify_user_sign_up_email"),
    path('verify_user_sign_up_otp/',verify_sign_up_otp, name="verify_user_sign_up_otp"),
    path('forgot_password_user/',forgot_password_user, name="forgot_password_user"),
    path('send_otp_for_password_view/',send_otp_for_password_view, name="send_otp_for_password_view"),
    path('forgot_password_reset_view/',forgot_password_reset_view, name="forgot_password_reset_view"),
]
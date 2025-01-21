from django.urls import path

from Ecommerce.admin_panel.users.views import admin_signup_view
from Ecommerce.admin_panel.users.views import admin_login_view
from Ecommerce.admin_panel.users.views import admin_logout_view
from Ecommerce.admin_panel.users.views import password_reset_view
from Ecommerce.admin_panel.users.views import delete_account_view
from Ecommerce.admin_panel.users.views import client_report_list_view
from Ecommerce.admin_panel.users.views import create_new_report_view
from Ecommerce.admin_panel.users.views import check_client_view
from Ecommerce.admin_panel.users.views import report_detail_view
from Ecommerce.admin_panel.users.views import report_update_view
from Ecommerce.admin_panel.users.views import reports_by_admin_view
from Ecommerce.admin_panel.users.views import report_search_suggestions_view
from Ecommerce.admin_panel.users.views import client_report_list_by_name_view
from Ecommerce.admin_panel.users.views import filter_reports_by_date
from Ecommerce.admin_panel.users.views import clear_report_session_data
from Ecommerce.admin_panel.users.views import forgot_password_view
from Ecommerce.admin_panel.users.views import reset_forgot_password_view
from Ecommerce.admin_panel.users.views import verify_sign_up_email
from Ecommerce.admin_panel.users.views import verify_sign_up_otp

urlpatterns = (
        path('admin_signup/', admin_signup_view, name='admin_signup'),
        path('', admin_login_view, name='admin_login'),
        path('admin_logout/', admin_logout_view, name='admin_logout'),
        path('password_reset/', password_reset_view, name='password_reset'),
        path('delete_account/', delete_account_view, name='delete_account'),
        path('client_report_list/', client_report_list_view, name='client_report_list'),
        path('create_new_report/', create_new_report_view, name='create_new_report'),
        path('check_client_view/<str:name>/', check_client_view, name='check_client_view'),
        path('report_detail/<int:report_id>/', report_detail_view, name='report_detail'),
        path('report_update_view/', report_update_view, name='report_update_view'),
        path('reports_by_admin/', reports_by_admin_view, name='reports_by_admin'),
        path('report_search_suggestions/', report_search_suggestions_view, name='report_search_suggestions'),
        path('client_report_list_by_name/', client_report_list_by_name_view, name='client_report_list_by_name'),
        path('filter_reports_by_date/', filter_reports_by_date, name='filter_reports_by_date'),
        path('clear_report_session_data/', clear_report_session_data, name='clear_report_session_data'),
        path('forgot_password_view/', forgot_password_view, name='forgot_password_view'),
        path('reset_forgot_password/', reset_forgot_password_view, name='reset_forgot_password'),
        path('verify_sign_up_email/', verify_sign_up_email, name='verify_sign_up_email'),
        path('verify_sign_up_otp/', verify_sign_up_otp, name='verify_sign_up_otp'),

)
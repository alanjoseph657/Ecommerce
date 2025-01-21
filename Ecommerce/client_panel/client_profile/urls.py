from django.urls import path

from Ecommerce.client_panel.client_profile.views import profile_page_view
from Ecommerce.client_panel.client_profile.views import update_user_profile
from Ecommerce.client_panel.client_profile.views import generate_otp_for_email_view
from Ecommerce.client_panel.client_profile.views import verify_otp_view
from Ecommerce.client_panel.client_profile.views import client_address_view
from Ecommerce.client_panel.client_profile.views import add_edit_address_view
from Ecommerce.client_panel.client_profile.views import delete_address_view


urlpatterns = [
  path('profile/',profile_page_view, name="profile"),
  path('update_user_profile/',update_user_profile, name="update_user_profile"),
  path('generate_otp_for_email_view/',generate_otp_for_email_view, name="generate_otp_for_email_view"),
  path('verify_otp_view/',verify_otp_view, name="verify_otp_view"),
  path('client_address_view/',client_address_view, name="client_address_view"),
  path('add_edit_address_view/',add_edit_address_view, name="add_edit_address_view"),
  path('delete_address_view/',delete_address_view, name="delete_address_view"),
]
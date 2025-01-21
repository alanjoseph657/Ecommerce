from django.urls import path

from Ecommerce.client_panel.homepage.views import homepage_view
from Ecommerce.client_panel.homepage.views import about_page_view
from Ecommerce.client_panel.homepage.views import privacy_policy_view
from Ecommerce.client_panel.homepage.views import terms_of_use_page_view
from Ecommerce.client_panel.homepage.views import returns_policy_view
from Ecommerce.client_panel.homepage.views import contact_us_view


urlpatterns = [
    path('', homepage_view, name='homepage_view'),
    path('about/', about_page_view, name='about'),
    path('privacy_policy/', privacy_policy_view, name='privacy_policy'),
    path('terms_of_use_page/', terms_of_use_page_view, name='terms_of_use_page'),
    path('returns_policy/', returns_policy_view, name='returns_policy'),
    path('contact_us/', contact_us_view, name='contact_us'),

]
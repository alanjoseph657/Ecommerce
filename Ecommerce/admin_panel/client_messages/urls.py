from django.urls import path

from Ecommerce.admin_panel.client_messages.views import messages_page_view
from Ecommerce.admin_panel.client_messages.views import message_detail_view
from Ecommerce.admin_panel.client_messages.views import update_message_status

urlpatterns = [
    path('messages_page/', messages_page_view, name="messages_page"),
    path('message_detail/<int:message_id>/', message_detail_view, name="message_detail"),
    path('update_message_status/', update_message_status, name="update_message_status"),
]
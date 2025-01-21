from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from Ecommerce.dataaccess.ecommerce_access.user_da import ClientMessagesDA, UserDA


class ClientMessagesBL():
    def __init__(self):
        pass

    def get_all_messages_bl(self, request, item_per_page=10):
        response = {"error": None, "success": False, "msg": ""}
        page_number = request.GET.get('page',1)
        search_date = request.GET.get('search_date')

        try:
            client_messages = ClientMessagesDA().get_all_messages()

            if search_date:
                client_messages = client_messages.filter(created_at__date=search_date)

            if client_messages:
                paginator = Paginator(client_messages, item_per_page)

                try:
                    paginated_messages = paginator.page(page_number)
                except PageNotAnInteger:
                    paginated_messages = paginator.page(1)
                except EmptyPage:
                    paginated_messages = paginator.page(paginator.num_pages)
                
                response['success'] = True
                response['client_messages'] = paginated_messages
            else:
                response['error'] = "No messages"
        except Exception as err:
            exception = str(err)
            response['error'] = "No messages"
        return response
    
    def get_message_detail_bl(self, request, message_id):
        response = {"error": None, "success": False, "msg": "", "updated": None}

        try:
            message_detail = ClientMessagesDA().get_message_detail_by_id(message_id)
            if message_detail:
                admin_id = message_detail.updated_by
                if admin_id:
                    admin_name = UserDA().get_user_by_id(admin_id)
                    response['updated'] = admin_name.username
                response['success'] = True
                response['message_detail'] = message_detail
        except Exception as err:
            exception = str(err)
            response['error'] = "Failed to fetch message detail"
        return response
    
    def upate_message_status_bl(self, request):
        response = {"error": None, "success": False, "msg": ""}
        user_id = request.user.id
        message_id = request.POST.get('message_id')
        status = request.POST.get('status')

        try:
            data_dict = {
                'updated_by': user_id,
                'status' : status
            }
            updated = ClientMessagesDA().update_message_details(message_id, data_dict)
            if updated:
                response['success'] = True
            else:
                response['error'] = "Failed to update"
        except Exception as err:
            exception = str(err)
            response['error'] = "Failed to update"
        return response


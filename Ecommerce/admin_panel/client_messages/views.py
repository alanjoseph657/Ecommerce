from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Ecommerce.common.decorator import admin_required
from Ecommerce.admin_panel.client_messages.client_messages_biz import ClientMessagesBL


@login_required(login_url='admin_login')
@admin_required
def messages_page_view(request):
    response = ClientMessagesBL().get_all_messages_bl(request)
    context = {
        'client_messages': response.get('client_messages')
    }
    return render(request, "client_messages.html", context)


@login_required(login_url='admin_login')
@admin_required
def message_detail_view(request, message_id):
    response = ClientMessagesBL().get_message_detail_bl(request, message_id)
    if response['error']:
        messages.warning(request, response.get('error'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'messages_page/'))
    context = {
        'message_detail': response.get('message_detail'),
        'updated' : response.get('updated'),
        'status_options' : ["OPEN", "REPLIED", "CLOSED"]
    }
    return render(request, "messages_detail.html", context)


@login_required(login_url='admin_login')
@admin_required
def update_message_status(request):
    response = ClientMessagesBL().upate_message_status_bl(request)
    if response['error']:
        messages.warning(request, response.get('error'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'dashboard_view'))
    return redirect(messages_page_view)

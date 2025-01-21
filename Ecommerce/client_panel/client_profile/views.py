from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Ecommerce.client_panel.client_profile.client_profile_biz import ProfileBL
from Ecommerce.client_panel.client_profile.client_profile_biz import AddressBL

@login_required(login_url='login')
def profile_page_view(request):
    response = ProfileBL().get_user_profile_bl(request)
    return render(request, "profile_page.html",{'user':response.get('user'), 'profile':response.get('profile')})


@login_required(login_url='login')
def update_user_profile(request):
    response = ProfileBL().update_user_profile_bl(request)
    if response['error']:
        messages.error(request, response.get('error'))
    return redirect(profile_page_view)


@login_required(login_url='login')
def generate_otp_for_email_view(request):
    response = ProfileBL().generate_otp_for_email_change(request)
    return JsonResponse(response)


@login_required(login_url='login')
def verify_otp_view(request):
    response = ProfileBL().verify_otp_for_email_change(request)
    return JsonResponse(response)


@login_required(login_url='login')
def client_address_view(request):
    response = AddressBL().get_address_for_user_bl(request)
    return render(request, "address.html",{'addresses':response.get('addresses')})


@login_required(login_url='login')
def add_edit_address_view(request):
    response = AddressBL().add_edit_address_bl(request)
    if response['error']:
        messages.error(request, response.get('error'))
    return redirect(client_address_view)


@login_required(login_url='login')
def delete_address_view(request):
    response = AddressBL().delete_address_bl(request)
    if response['error']:
        messages.error(request, response.get('error'))
    return redirect(client_address_view)
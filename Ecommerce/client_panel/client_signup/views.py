from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from Ecommerce.client_panel.client_signup.login_biz import UserBL
from Ecommerce.common.forms import CaptchaForm

def login_page(request):
    if request.method == 'POST':
        response = UserBL().login_user_bl(request)
        if response['success']:
            return redirect("homepage_view")
        else:
            messages.error(request,response.get('error'))
    return render(request, "client_login.html")


def logout_user_view(request):
    response = UserBL().logout_user_bl(request)
    if response['success']:
        return redirect(login_page)
    else:
        messages.error(request, response.get('error'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def sign_up_user(request):
    if request.method == "POST":
        response = UserBL().sign_up_user_bl(request)
        if response['success']:
            return redirect(login_page)
        else:
            messages.error(request, response.get('error'))
    captcha_form = CaptchaForm()
    return render(request,"client_signup.html", {'captcha_form': captcha_form})


def verify_sign_up_email(request):
    response = UserBL().generate_otp_for_sign_up(request)
    return JsonResponse(response)


def verify_sign_up_otp(request):
    response = UserBL().verify_sign_up_otp_bl(request)
    return JsonResponse(response)


def send_otp_for_password_view(request):
    response = UserBL().send_otp_mail_bl(request)
    return JsonResponse(response)
    

def forgot_password_user(request):
    response = UserBL().verify_sent_otp_password(request)
    if response['success']:
        return render(request,"client_forgot_password.html")
    messages.error(request, response.get('error'))
    print(response)
    return redirect(login_page)


def forgot_password_reset_view(request):
    response = UserBL().reset_forgot_password_bl(request)
    if response['success']:
        return redirect(login_page)
    else:
        messages.error(request,response.get('error'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
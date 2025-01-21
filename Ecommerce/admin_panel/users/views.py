from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from Ecommerce.admin_panel.users.users_biz import UserBL
from Ecommerce.admin_panel.users.users_biz import ClientReportBL
from Ecommerce.common.decorator import admin_required
from Ecommerce.common.forms import CaptchaForm


def admin_signup_view(request):
    if request.method == "POST":
        result = UserBL().sign_up_admin_user(request)
        if result['success']:
            messages.success(request,"Sign Up Success")
            return redirect(admin_login_view)
        messages.error(request,result.get('error'))
    captcha_form = CaptchaForm()
    return render(request, "signup_page.html", {'captcha_form': captcha_form})


def verify_sign_up_email(request):
    response = UserBL().generate_otp_for_sign_up(request)
    return JsonResponse(response)


def verify_sign_up_otp(request):
    response = UserBL().verify_sign_up_otp_bl(request)
    return JsonResponse(response)


def admin_login_view(request):
    if request.method == "POST":
        response = UserBL().login_admin_user(request)
        if response['success']:
            return redirect('dashboard_view')
        messages.warning(request, response.get('error'))
    return render(request,"login_page.html")


@login_required(login_url='admin_login')
def admin_logout_view(request):
    response = UserBL().logout_admin_user(request)
    if response['success']:
        return redirect(admin_login_view)
    messages.warning(request, response.get('error'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'dashboard_view'))


@login_required(login_url='admin_login')
def password_reset_view(request):
    if request.method == "POST":
        response = UserBL().reset_admin_password(request)
        if response['success']:
            messages.success(request, response.get('msg'))
        else:
            messages.warning(request, response.get('error'))
    return render(request, "password_reset.html")


@login_required(login_url='admin_login')
def delete_account_view(request):
    response = UserBL().delete_account_bl(request)
    if response['success']:
        messages.success(request, response.get('msg'))
        return redirect(admin_login_view)
    else:
        messages.warning(request, response.get('error'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'dashboard_view'))
    

@login_required(login_url='admin_login')
@admin_required
def create_new_report_view(request):
    if request.method == "POST":
        response = ClientReportBL().create_report_bl(request)
        if response['success']:
            messages.success(request, response.get('msg'))
        else:
            messages.warning(request, response.get('error'))
    return render(request, "create_report.html")


def check_client_view(request, name):
    response = UserBL().check_client_exist_bl(name)
    return JsonResponse(response)


@login_required(login_url='admin_login')
@admin_required
def report_detail_view(request, report_id):
    response = ClientReportBL().report_detail_bl(report_id)
    if response['success']:
        return render(request,"report_view.html",{'result': response})
    else:
        messages.warning(request, response.get('error'))
    return redirect(client_report_list_view)


@login_required(login_url='admin_login')
@admin_required
def report_update_view(request):
    if request.method == "POST":
        response = ClientReportBL().report_edit_bl(request)
        if response['success']:
            messages.success(request, response.get('msg'))
        else:
            messages.warning(request, response.get('error'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'client_report_list/'))


@login_required(login_url='admin_login')
@admin_required
def reports_by_admin_view(request):
    result = ClientReportBL().list_all_client_report_by_admin_bl(request)
    if result['error']:
        messages.warning(request, result.get('error'))
    return render(request,"your_reports.html",{'result': result.get('reports')})


def report_search_suggestions_view(request):
    response = ClientReportBL().report_search_suggestions_bl(request)
    return JsonResponse(response, safe=False)


@login_required(login_url='admin_login')
@admin_required
def client_report_list_view(request):
    result = ClientReportBL().list_all_client_report_bl(request)
    if result['error']:
        messages.warning(request, result.get('error'))
    return render(request,"client_report_list.html",{'result': result.get('reports')})


# unused
@login_required(login_url='admin_login')
@admin_required
def client_report_list_by_name_view(request):
    result = ClientReportBL().list_all_client_report_by_name_bl(request)
    if result['error']:
        messages.warning(request, result.get('error'))
    return render(request,"client_report_list.html",{'result': result.get('reports')})

# unused
@login_required(login_url='admin_login')
@admin_required
def filter_reports_by_date(request):
    date = request.POST.get('search-date')
    page_number = request.POST.get('page_number', 1)
    result = ClientReportBL().list_reports_by_date_bl(request, search_date=date, page_number=page_number)
    reports_html = render_to_string('partials/reports_table.html', {'result': result})
    paginator = result.paginator
    return JsonResponse({'reports_html': reports_html, 'paginator': paginator})

# unused
def clear_report_session_data(request):
    if 'search_report' in request.session:
        del request.session['search_report']
    if 'search_date' in request.session:
        del request.session['search_date']
    return JsonResponse({'status': 'success'})


def forgot_password_view(request):
    if request.method == "POST":
        opt_verified = UserBL().verify_otp_bl(request)
        if opt_verified['success']:
            return render(request,"forgot_password_reset.html")
        else:
            messages.warning(request, opt_verified.get('error'))
            return redirect(admin_login_view)
    result = UserBL().send_otp_mail_bl(request)
    if result['error']:
        messages.warning(request, result.get('error'))
        return redirect(admin_login_view)
    return render(request, "otp_verification.html")


def reset_forgot_password_view(request):
    result = UserBL().reset_forgot_admin_password_bl(request)
    if result['error']:
        messages.warning(request, result.get('error'))
    else:
        messages.success(request, result.get('msg'))
    return redirect(admin_login_view)

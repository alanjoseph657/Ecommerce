from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from stripe import Charge
import stripe

from Ecommerce.client_panel.client_order.order_biz import OrderBL


def payment_page_view(request):
    return render(request, "payment.html",{'order_id':request.GET.get('order_id')})


@login_required(login_url='login')
def client_orders_view(request):
    response = OrderBL().get_orders_by_user_bl(request)
    return render(request,"client_orders.html",{'orders' : response.get('orders')})


@login_required(login_url='login')
def place_order_views(request):
    response = OrderBL().place_order_bl(request)
    if response['error']:
        messages.error(request, response.get('error'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(client_orders_view)
    

@login_required(login_url='login')
def order_detail_view(request):
    response = OrderBL().get_order_detail_bl(request)
    context = {
        'items' : response.get('items'),
        'order' : response.get('order'),
        'address' : response.get('address')
    }
    return render(request, "client_order_detail.html", context)


@login_required(login_url='login')
def cancel_order_view(request):
    response = OrderBL().cancel_order_bl(request)
    return redirect(client_orders_view)


def process_payment(request):
    if request.method == "POST":
        token = request.POST.get('token')
        amount = int(request.POST.get('amount'))
        currency = request.POST.get('currency')

        try:
            charge = Charge.create(
                amount=amount,
                currency=currency,
                source=token,
                description='Test payment'
            )
            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            return JsonResponse({'success': False, 'error': e.message})
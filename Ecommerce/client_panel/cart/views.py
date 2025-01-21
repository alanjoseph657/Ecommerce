from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Ecommerce.client_panel.cart.cart_biz import CartBl
from Ecommerce.client_panel.client_profile.client_profile_biz import AddressBL


@login_required(login_url='login')
def cart_page_view(request):
    if request.method == "POST":
        response = CartBl().add_product_to_cart_bl(request)
        if response['error']:
            messages.error(request, response.get('error'))
    
    result = CartBl().get_cart_for_user_bl(request)
    address = AddressBL().get_shipping_address_bl(request)
    context = {
        'result':result,
        'addresses': address.get('addresses'),
        'shipping_address' : address.get('shipping_address').first()
    }
    return render(request, "cart.html",context)


def remove_from_cart_view(request):
    response = CartBl().remove_from_cart_bl(request)
    return redirect(cart_page_view)


def get_address_by_id_for_cart_view(request):
    response = AddressBL().get_address_values_for_cart_bl(request)
    return JsonResponse(response, safe=False)


def proceed_checkout_view(request):
    response = CartBl().proceed_checkout_bl(request)
    return JsonResponse(response)
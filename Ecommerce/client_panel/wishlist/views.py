import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string

from Ecommerce.client_panel.wishlist.wishlist_biz import WishlistBL


@login_required(login_url='login')
def get_wishlist_view(request):
    response = WishlistBL().get_user_wishlist_bl(request)
    if 'ajax' in request.GET:
        return HttpResponse(json.dumps({
            'html' : render_to_string("partials/partial_wishlist.html",{'wishlist': response.get('wishlist')}),
            'next_page_number': response.get('next_page_number'),
            'has_next': response.get('has_next')
        }))
    return render(request, "wishlist.html", 
                {'wishlist': response.get('wishlist'),
                'next_page_number': response.get('next_page_number'),
                'has_next': response.get('has_next')})


@login_required(login_url='login')
def add_to_wishlist_view(request):
    response = WishlistBL().add_to_wishlist_bl(request)
    if response['success']:
        messages.success(request, response.get('msg'))
        return redirect(get_wishlist_view)
    else:
        messages.error(request, response.get('error'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    

@login_required(login_url='login')
def remove_from_wislist_view(request):
    response = WishlistBL().remove_from_wishlist_bl(request)
    return redirect(get_wishlist_view)

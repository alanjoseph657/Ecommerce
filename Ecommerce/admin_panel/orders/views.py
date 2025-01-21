from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from Ecommerce.common.decorator import admin_required
from Ecommerce.admin_panel.orders.orders_biz import OrderBL


@login_required(login_url='admin_login')
@admin_required
def list_order_view(request):
    response = OrderBL().list_all_orders_bl(request)
    if response['error']:
        messages.warning(request,response.get('error'))
    return render(request, "orders_list.html", {'result': response})


# unused
@login_required(login_url='admin_login')
@admin_required
def list_order_status_filter_view(request, status):
    response = OrderBL().list_all_orders_bl(request, status=status)
    # if response['error']:
    #     messages.warning(request,response['error'])
    html_table = render_to_string('partials/order_table_body.html', {'result': response})
    html_pagination = render_to_string('partials/pagination_partial.html', {'result': response})
    return JsonResponse({'html_table': html_table, 'html_pagination': html_pagination})


@login_required(login_url='admin_login')
@admin_required
def search_order_by_number_view(request):
    if request.method == "POST":
        if 'search_number' in request.session:
            del request.session['search_number']
    response = OrderBL().search_orders_by_reference(request)
    if response['error']:
        messages.warning(request,response.get('error'))
    return render(request, "orders_list.html", {'result': response})
    

@login_required(login_url='admin_login')
@admin_required
def order_detail_view(request, order_id):
    response = OrderBL().order_detail_bl(order_id)
    if response['error']:
        messages.warning(request, response.get('error'))
        return redirect(list_order_view)
    context = {
        'order': response.get('order'),
        'order_item': response.get('orderitem'),
        'user': response.get('user'),
        'address' : response.get('address')
    }
    return render(request, "order_detail.html", context)


@login_required(login_url='admin_login')
@admin_required
def view_order_by_product(request):
    if request.method == 'POST':
        search_query = request.POST.get('search-query')
        request.session['search_query'] = search_query
    else:
        search_query = request.session.get('search_query', '')
    response = OrderBL().order_list_by_product_bl(request,query=search_query)
    if response['success']:
        return render(request, "order_by_products.html", {'result': response})
    else:
        messages.warning(request, response.get('error'))
    return render(request, "order_by_products.html")


@login_required(login_url='admin_login')
@admin_required
def order_by_product(request):
    if 'search_query' in request.session:
        del request.session['search_query']
    return render(request, "order_by_products.html")

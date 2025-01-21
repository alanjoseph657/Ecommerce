from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Ecommerce.common.decorator import admin_required
from Ecommerce.admin_panel.inventory.inventory_biz import InventoryBL


@login_required(login_url='admin_login')
@admin_required
def list_inventory_view(request):
    result = InventoryBL().get_inventory_list_bl(request)
    context = {
        'inventory': result.get('paginated_inventory'),
        'product' : result.get('products'),
        'inventory_count' : result.get('inventory_count'),
        'variants' : result.get('variants')
    }
    if result['error']:
        messages.warning(request,result.get('error'))
    return render(request,"list_inventory.html",context)


@login_required(login_url='admin_login')
@admin_required
def update_inventory_view(request, inventory_id):
    response = InventoryBL().get_inventory_data_bl(inventory_id)
    if request.method == 'POST':
        response = InventoryBL().update_inventory_record_bl(request, inventory_id)
        if response['success']:
            messages.success(request,response.get('msg'))
            return redirect(list_inventory_view)
        else:
            messages.warning(request, response.get('error'))
    return render(request, "update_inventory_record.html",{'result': response.get('inventory')})


# unused
def inventory_list_by_product_search_view(request):
    if request.method == 'POST':
        search_query = request.POST.get('search-query')
        request.session['search_query'] = search_query
    else:
        search_query = request.session.get('search_query', '')
    result = InventoryBL().get_inventory_list_bl(request,query = search_query)
    context = {
    'inventory': result.get('paginated_inventory'),
    'product' : result.get('products'),
    'inventory_count' : result.get('inventory_count'),
    'variants' : result.get('variants')
    }
    if result['error']:
        messages.warning(request,result.get('error'))
    return render(request,"list_inventory.html",context)


from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from Ecommerce.common.decorator import admin_required
from Ecommerce.admin_panel.products.product_biz import ProductBL
from Ecommerce.admin_panel.products.product_biz import CategoryBL


@login_required(login_url='admin_login')
@admin_required
def add_product_view(request):
    categories = CategoryBL().get_category_dropdown()
    if request.method == 'POST':
        response = ProductBL().add_product_bl(request)
        if response['success']:
            messages.success(request,response.get('msg'))
            return redirect(list_all_products_view)
        else:
            messages.warning(request,response.get('error')) 
    return render(request,"add_product.html",{'categories': categories})


@login_required(login_url='admin_login')
@admin_required
def update_product_data_view(request, slug):
    product = ProductBL().get_product_detail(slug)
    categories = CategoryBL().get_category_dropdown()
    context = {
        'product':product.get('product'),
        'media':product.get('media'),
        'categories': categories
    }
    return render(request,"update_product.html", context)


@login_required(login_url='admin_login')
@admin_required
def edit_product_detail_form(request, product_id ):
    if request.method == "POST":
        response = ProductBL().update_product_bl(request, product_id)
        if response['success']:
            messages.success(request, response.get('msg'))
        else:
            messages.warning(request, response.get('error'))
    return redirect(reverse('product_detail', kwargs = {'slug':response.get('slug')}))
        

@login_required(login_url='admin_login')
@admin_required
def edit_product_gallery_form(request, product_id):
    if request.method == "POST":
        response = ProductBL().update_product_media_bl(request, product_id)   
        if response['success']:
            messages.success(request, response.get('msg'))
        else:
            messages.warning(request, response.get('error'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'list_all_products/'))


@login_required(login_url='admin_login')
@admin_required
def list_all_products_view(request):
    categories = CategoryBL().get_category_dropdown()
    categories_dict = {cat[0]:cat[1] for cat in categories}
    result = ProductBL().list_product_bl(request)
    if result.get('error'):
        messages.warning(request,result.get('error'))
    return render(request,"list_products.html",{'result':result,'categories':categories,'categories_dict':categories_dict})


@login_required(login_url='admin_login')
@admin_required
def delete_product_view(request, slug):
    response = ProductBL().delete_product_bl(slug)
    if response['success']:
        messages.success(request, response.get('msg'))
    else:
        messages.warning(request, response.get('error'))
    return redirect(list_all_products_view)
    

@login_required(login_url='admin_login')
@admin_required
def product_detail_view(request, slug):
    response = ProductBL().get_product_detail(slug)
    if response['success']:
        product = response.get('product')
        media = response.get('media')
        variants = response.get('variants')
        context = {'product':product,'media':media,'variants':variants}
        return render(request,"product_detail.html",context)

    else:
        messages.warning(request,response.get('error'))
        return render(request,"product_detail.html")


@login_required(login_url='admin_login')
@admin_required
def add_variant_view(request,product_id):
    response = ProductBL().add_product_variant_bl(request,product_id)
    if response['success']:
        messages.success(request,response.get('msg'))
    else:
        messages.warning(request,response.get('error'))
    return JsonResponse(response)


@login_required(login_url='admin_login')
@admin_required
def update_variant_view(request):
    response = ProductBL().update_product_variant_bl(request)
    if response['success']:
        messages.success(request,response.get('msg'))
    else:
        messages.warning(request,response.get('error'))
    return JsonResponse(response)


@login_required(login_url='admin_login')
@admin_required
def delete_variant_view(request, variant_id):
    response = ProductBL().delete_variant_bl(variant_id)
    if response['success']:
        messages.success(request,response.get('msg'))
    else:
        messages.warning(request,response.get('error'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'dashboard_view'))

# unused
def search_product_name_view(request):
    if request.method == 'POST':
        search_query = request.POST.get('search-query')
        request.session['search_query'] = search_query
    else:
        search_query = request.session.get('search_query', '')
    result = ProductBL().search_product_using_name_bl(request,query=search_query)
    categories = CategoryBL().get_category_dropdown()
    categories_dict = {cat[0]:cat[1] for cat in categories}
    if result.get('error'):
        messages.warning(request,result.get('error'))
    return render(request,"list_products.html",{'result':result,'categories':categories,'categories_dict':categories_dict})


@login_required(login_url='admin_login')
@admin_required
def product_status_change_view(request):
    response = ProductBL().check_status_change(request)
    return JsonResponse(response)


def product_search_suggestions_view(request):
    response = ProductBL().product_search_suggestion(request)
    return JsonResponse(response, safe=False)
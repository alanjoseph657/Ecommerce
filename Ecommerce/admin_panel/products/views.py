from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Ecommerce.common.decorator import admin_required
from Ecommerce.admin_panel.products.product_biz import CategoryBL

@login_required(login_url='admin_login')
@admin_required
def create_category_view(request):
    if request.method == 'POST':
        response = CategoryBL().create_category(request)
        if response['success']:
            messages.success(request,response.get('msg'))
            return redirect(list_all_categories_view)
        else:
            messages.warning(request,response.get('error'))
    return render(request,"create_category.html")


@login_required(login_url='admin_login')
@admin_required
def list_all_categories_view(request):
    result = CategoryBL().list_categories(request)
    if result['error']:
        messages.warning(request,result.get('error'))
    return render(request,"list_categories.html",{'result' : result})


@login_required(login_url='admin_login')
@admin_required
def update_category_view(request, slug):
    category_data = CategoryBL().category_data_by_slug(slug)
    if request.method == 'POST':
        response = CategoryBL().update_category(request,slug)
        if response['success']:
            messages.success(request,response.get('msg'))
            return redirect(list_all_categories_view)
        else:
            messages.warning(request,response.get('error'))
            return render(request, "update_category.html", {'category_data' : category_data ,'response': response, 'slug': slug})
    return render(request,"update_category.html", {'category_data' : category_data , 'slug': slug})


@login_required(login_url='admin_login')
@admin_required
def delete_category_view(request, slug):
    category = CategoryBL().delete_category_by_slug(slug)
    if category['success']:
        messages.success(request,category.get('msg'))
    else:
        messages.warning(request,category.get('error'))
    return redirect(list_all_categories_view)

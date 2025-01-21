import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from Ecommerce.client_panel.client_products.products_biz import ProductBL


def products_view(request):
    result = ProductBL().get_all_products_bl(request)
    if 'ajax' in request.GET:
        return HttpResponse(json.dumps({
            'html' : render_to_string("partials/partial_products.html",{'products': result.get('products')}),
            'next_page_number': result.get('next_page_number'),
            'has_next': result.get('has_next')
        }))
    return render(request, "products.html", 
                {'products': result.get('products'),
                'next_page_number': result.get('next_page_number'),
                'has_next': result.get('has_next')})


def more_products(request):
    response = ProductBL().get_all_products_bl()
    products = response.get('products', [])
    offset = int(request.GET.get('offset', 0))
    products = products[offset:offset + 10]    
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.product_name,
            'price': product.price,
            'image': product.product_media,
            'slug' : product.slug
        })
    return JsonResponse(data, safe=False)


def product_detail_view(request,slug):
    result = ProductBL().get_product_details_bl(slug)
    related_products = ProductBL().get_related_products_bl(slug)

    context = {
        'product' : result.get('products'),
        'variants' : result.get('variants'),
        'media' : result.get('media'),
        'category' : result.get('category'),
        'related' : related_products.get('related')
    }
    return render(request,"client_product_detail.html",context)


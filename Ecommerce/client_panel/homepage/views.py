from django.shortcuts import render
from django.contrib import messages

from Ecommerce.client_panel.homepage.homepage_biz import HomepageBL

def homepage_view(request):
    category = HomepageBL().get_categories_bl()
    products = HomepageBL().get_latest_products_bl()
    request.session['categories'] = category.get('categories')
    most_ordered = HomepageBL().get_most_oredered_of_month_bl()
    
    context = {
        'products':products.get('products'),
        'most_ordered_product' : most_ordered.get('product_details'),
        'most_ordered_image' : most_ordered.get('product_media')
    }
    return render(request, "homepage.html", context)


def about_page_view(request):
    return render(request, "about_us.html")


def privacy_policy_view(request):
    return render(request, "privacy_policy.html")


def terms_of_use_page_view(request):
    return render(request, "terms_of_use.html")


def returns_policy_view(request):
    return render(request, "return_policy.html")


def contact_us_view(request):
    if request.method == "POST":
        response = HomepageBL().add_new_client_message_bl(request)
        if response['success']:
            messages.success(request, response.get('msg'))
        else:
            messages.error(request, response.get('error'))
    return render(request,"contact.html")
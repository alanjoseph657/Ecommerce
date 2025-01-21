from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from Ecommerce.common.decorator import admin_required

from Ecommerce.admin_panel.dashboard.dashboard_biz import DashboardBL

@login_required(login_url='admin_login')
@admin_required
def dashboard_view(request):
    result = DashboardBL().count_cards_bl()
    recent_history = DashboardBL().recent_inventory_actions_bl()
    # history_graph = json.dumps(DashboardBL().history_for_7_days(7))   
    client_reports = DashboardBL().dashboard_client_reports_bl()
    products = DashboardBL().dashboard_products_bl()
    product_detail = DashboardBL().most_ordered_product_bl()
    order_status = DashboardBL().order_status_bl()
    
    context={
        'result':result,
        'recent_history': recent_history.get('recent_history'),
        'client_reports' : client_reports.get('reports'),
        'products' : products.get('products'),
        'product_detail' : product_detail.get('product_details'),
        'product_media' : product_detail.get('product_media'),
        'order_status' : order_status.get('order_status'),
        # 'history_graph' : history_graph
    }
    return render(request, "index.html", context)


def get_inventory_chart(request):
    days = request.GET.get('days')
    history_graph =DashboardBL().history_for_7_days(int(days))
    return JsonResponse(history_graph, safe=False)
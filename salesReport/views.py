from django.shortcuts import render
from products.models import Orders
from django.db.models import Sum, Count
# Create your views here.
from django.db.models.functions import TruncDate, TruncMonth
from .forms import DateRangeForm


# def sales_report(request):
#     orders = Orders.objects.all()
#     labels = []
#     data = []
#     sales_data = Orders.objects.values('order_date__month').annotate(total_sales=Sum('total_amount'))
#     # print("chart data: ",sales_data)
    
#     for order in orders:
#         labels.append(order.username)
#         data.append(order.total_amount)

#     # Create a dictionary to store the sales data
#     sales_data_dict = {}
#     for entry in sales_data:
#         month = entry['order_date__month']
#         total_sales = entry['total_sales']
#         sales_data_dict[month] = total_sales
#     context = {
#         'orders' : orders,
#         # 'sales_data': sales_data_dict
#         "labels": labels,
#         "data" : data,
#     }
#     print("labels : ", labels, "data : ", data)
#     return render(request, "salesReport/sales_report.html", context)


def sales_report(request):
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_month = form.cleaned_data["start_month"]
            end_month = form.cleaned_data["end_month"]
            print("start_month : ", start_month, "end_month : ", end_month)
    else:
        form = DateRangeForm()
    orders = Orders.objects.all()
    
    daily_sales_data = Orders.objects.annotate(
        order_date_day=TruncDate('order_date')
    ).values('order_date_day').annotate(
        total_sales=Sum('orderitems__selling_price'),
        sales_count=Count('id')
    ).order_by('order_date_day')
    
    formatted_dates = [entry['order_date_day'].strftime('%d-%B') for entry in daily_sales_data]
    sales_count = [entry['sales_count'] for entry in daily_sales_data]
    total_amounts = [float(entry['total_sales']) for entry in daily_sales_data]
    
    
    monthly_sales_data = Orders.objects.annotate(
        order_date_month=TruncMonth('order_date')
    ).values('order_date_month').annotate(
        total_sales=Sum('orderitems__selling_price')
    ).order_by('order_date_month')

    formatted_months = [entry['order_date_month'].strftime('%B %Y') for entry in monthly_sales_data]
    total_monthly_sales = [float(entry['total_sales']) for entry in monthly_sales_data]

    context = {
        "daily_sales_data" : daily_sales_data,
        "orders" : orders,
        "dates": formatted_dates,
        "total_amounts": total_amounts,
        "total_monthly_sales" : total_monthly_sales,
        "formatted_months" : formatted_months,
        "sales_count" : sales_count,
        "form" : form,
    }
    
    return render(request, "salesReport/sales_report.html", context)


# from decimal import Decimal

# def sales_report(request):
#     orders = Orders.objects.all()
#     daily_sales_data = Orders.objects.annotate(
#         order_date_day=TruncDate('order_date')
#     ).values('order_date_day').annotate(
#         total_sales=Sum('orderitems__selling_price')
#     ).order_by('order_date_day')

#     # Convert the data to a format that JavaScript understands
#     daily_sales_data_json = json.dumps([
#         {
#             'order_date_day': data['order_date_day'].strftime('%Y-%m-%d'),
#             'total_sales': float(data['total_sales']),
#         }
#         for data in daily_sales_data
#     ])

#     context = {
#         "daily_sales_data": daily_sales_data,
#         "orders": orders,
#         'daily_sales_data_json': daily_sales_data_json,
#         'day_number': [1, 2, 3, ...],  
#         'total_order': [10, 20, 30, ...]
#     }

#     return render(request, "salesReport/sales_report.html", context)
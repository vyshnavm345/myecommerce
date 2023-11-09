from django.shortcuts import render
from products.models import Orders
from django.db.models import Sum, Count
# Create your views here.
from django.db.models.functions import TruncDate, TruncMonth
from .forms import DateRangeForm
from django.db.models import Q


def sales_report(request):
    orders = Orders.objects.all()
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_month = form.cleaned_data["start_month"]
            end_month = form.cleaned_data["end_month"]
            
             # Get daily sales data between start_month and end_month
            daily_sales_data = Orders.objects.annotate(
                order_date_day=TruncDate('order_date')
            ).values('order_date_day').annotate(
                total_sales=Sum('orderitems__selling_price'),
                sales_count=Count('id')
            ).order_by('order_date_day').filter(
                Q(order_date_day__gte=start_month) & Q(order_date_day__lte=end_month)
            )
            
            formatted_dates = [entry['order_date_day'].strftime('%d-%B') for entry in daily_sales_data]
            sales_count = [entry['sales_count'] for entry in daily_sales_data]
            total_amounts = [float(entry['total_sales']) for entry in daily_sales_data]
            
            monthly_sales_data = Orders.objects.annotate(
                order_date_month=TruncMonth('order_date')
            ).values('order_date_month').annotate(
                total_sales=Sum('orderitems__selling_price')
            ).order_by('order_date_month').filter(
                Q(order_date_month__gte=start_month) & Q(order_date_month__lte=end_month)
            )

            formatted_months = [entry['order_date_month'].strftime('%B %Y') for entry in monthly_sales_data]
            total_monthly_sales = [float(entry['total_sales']) for entry in monthly_sales_data]
    else:
        form = DateRangeForm()
        
        
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

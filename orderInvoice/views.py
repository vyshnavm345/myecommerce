from django.shortcuts import render , get_list_or_404
from django.contrib.auth.decorators import login_required
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse

from xhtml2pdf import pisa
from products.models import Orders, OrderItems

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    
    if not pdf.err:
        return result.getvalue()
    return None

@login_required
def admin_order_pdf(request, order_id):
    
    # order = get_list_or_404(Orders, pk=order_id).first()
    order = Orders.objects.get(id=order_id)
    order_items = OrderItems.objects.filter(order=order)
    print("pdf order: ",order)
    print("pdf order: ",order.username)
    pdf = render_to_pdf('orderInvoice/order_pdf.html', {'order' : order, 'order_items' : order_items})
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=%s.pdf" % order_id
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not Found")
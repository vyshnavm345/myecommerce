from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.
def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('admin_order_pdf', args=[obj.id])))
    order_name.short_description = 'PDF Title'
                     
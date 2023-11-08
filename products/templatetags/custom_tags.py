from django import template
import time
register = template.Library()

@register.filter(name='subtract')
def subtract(a, b):
    return int(a) - int(b)
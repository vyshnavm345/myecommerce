from django import template

register = template.Library()

@register.filter
def calculate_total_price(product, quantity):
    return product.price * quantity
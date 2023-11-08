from django import template

register = template.Library()

@register.filter(name="offer_price")
def offer_price(price, disc_percentage):
    return int(price) - (int(price) * int(disc_percentage) / 100)


@register.filter
def get_attr(obj, attr_name):
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None
from django import template

register = template.Library()

@register.inclusion_tag('product_tile.html')
def product_tile(data):
    return {**data}

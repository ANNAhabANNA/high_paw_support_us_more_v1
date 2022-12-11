from django import template

register = template.Library()

# Calculates subtotal for products in shopping bag.
@register.filter(name='calculate_subtotal')
def calculate_subtotal(price, quantity):
    return price * quantity
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def precio_venta(precio):
    """Calcula el precio de venta recomendado (precio + 30%)"""
    try:
        precio_decimal = Decimal(str(precio))
        return precio_decimal * Decimal('1.30')
    except:
        return 0

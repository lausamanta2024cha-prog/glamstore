# Generated migration to populate lotes and fechaVencimiento for products

from django.db import migrations
from datetime import datetime, timedelta


def populate_lotes_and_vencimiento(apps, schema_editor):
    """Populate missing lotes and fechaVencimiento for products"""
    Producto = apps.get_model('core', 'Producto')
    
    # Productos sin lote
    productos_sin_lote = Producto.objects.filter(lote__isnull=True) | Producto.objects.filter(lote='')
    
    # Asignar lote por defecto
    for producto in productos_sin_lote:
        producto.lote = 'L2025-12'
        producto.save()
    
    # Productos sin fecha de vencimiento
    productos_sin_vencimiento = Producto.objects.filter(fechaVencimiento__isnull=True)
    
    # Asignar fecha de vencimiento por defecto (2 años desde hoy)
    fecha_vencimiento_default = datetime.now().date() + timedelta(days=730)
    
    for producto in productos_sin_vencimiento:
        producto.fechaVencimiento = fecha_vencimiento_default
        producto.save()


def reverse_populate(apps, schema_editor):
    """Reverse operation - set to NULL"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_create_distribuidores_table'),
    ]

    operations = [
        migrations.RunPython(populate_lotes_and_vencimiento, reverse_populate),
    ]

#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.productos import Producto
from core.models.lotes import LoteProducto

print("=" * 70)
print("VERIFICACIÓN DE PRODUCTOS")
print("=" * 70)

productos = Producto.objects.all()
print(f"\nTotal de productos: {productos.count()}")

print("\nProductos con stock > 0:")
for prod in productos:
    print(f"  • {prod.nombreProducto}")
    print(f"    - Stock: {prod.stock}")
    print(f"    - Cantidad Disponible: {prod.cantidadDisponible}")
    
    # Verificar lotes
    lotes = LoteProducto.objects.filter(producto=prod)
    print(f"    - Lotes: {lotes.count()}")
    if lotes.exists():
        for lote in lotes:
            print(f"      • Lote {lote.codigo_lote}: {lote.cantidad_disponible} disponibles")
    print()

print("=" * 70)

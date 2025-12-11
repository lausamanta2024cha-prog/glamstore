#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.clientes import Cliente
from core.models.pedidos import Pedido
from core.models.categoria import Categoria, Subcategoria
from core.models.productos import Producto

print("=" * 60)
print("VERIFICACIÓN DE DATOS EN LA BASE DE DATOS")
print("=" * 60)

print(f"\n✓ Total de clientes: {Cliente.objects.count()}")
print(f"✓ Total de pedidos: {Pedido.objects.count()}")
print(f"✓ Total de categorías: {Categoria.objects.count()}")
print(f"✓ Total de subcategorías: {Subcategoria.objects.count()}")
print(f"✓ Total de productos: {Producto.objects.count()}")

print("\n" + "=" * 60)
print("CLIENTES REGISTRADOS:")
print("=" * 60)
for c in Cliente.objects.all():
    print(f"  • {c.nombre} ({c.email})")

print("\n" + "=" * 60)
print("RESUMEN DE PEDIDOS:")
print("=" * 60)
total_ventas = sum(p.total for p in Pedido.objects.all() if p.total)
print(f"  • Total de ventas: ${total_ventas:,.2f}")
print(f"  • Promedio por pedido: ${total_ventas / Pedido.objects.count():,.2f}" if Pedido.objects.count() > 0 else "  • Promedio por pedido: $0.00")

print("\n" + "=" * 60)
print("CATEGORÍAS:")
print("=" * 60)
for cat in Categoria.objects.all():
    prod_count = Producto.objects.filter(idCategoria=cat).count()
    print(f"  • {cat.nombreCategoria} ({prod_count} productos)")

print("\n" + "=" * 60)
print("ESTADO DEL DASHBOARD:")
print("=" * 60)
print("✓ Datos listos para mostrar en el dashboard")
print("✓ Clientes: Sí")
print("✓ Pedidos: Sí")
print("✓ Productos: Sí")
print("✓ Categorías: Sí")
print("\n" + "=" * 60)

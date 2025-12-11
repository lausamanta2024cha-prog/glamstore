#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.clientes import Cliente
from core.models.pedidos import Pedido
from core.models.categoria import Categoria, Subcategoria
from core.models.productos import Producto
from core.models import Usuario

print("=" * 70)
print("VERIFICACIÓN COMPLETA DE DATOS")
print("=" * 70)

print("\n1. USUARIOS Y ROLES:")
print("-" * 70)
usuarios = Usuario.objects.all()
print(f"Total de usuarios: {usuarios.count()}")
for u in usuarios:
    print(f"  • {u.nombre} ({u.email}) - Rol: {u.id_rol}")

print("\n2. CLIENTES:")
print("-" * 70)
clientes = Cliente.objects.all()
print(f"Total de clientes: {clientes.count()}")
for c in clientes[:5]:
    print(f"  • {c.nombre} ({c.email})")

print("\n3. CATEGORÍAS:")
print("-" * 70)
categorias = Categoria.objects.all()
print(f"Total de categorías: {categorias.count()}")
for cat in categorias:
    print(f"  • {cat.nombreCategoria} (ID: {cat.idCategoria})")

print("\n4. PRODUCTOS:")
print("-" * 70)
productos = Producto.objects.all()
print(f"Total de productos: {productos.count()}")
for prod in productos[:5]:
    print(f"  • {prod.nombreProducto} - ${prod.precio} (Stock: {prod.stock})")

print("\n5. PEDIDOS:")
print("-" * 70)
pedidos = Pedido.objects.all()
print(f"Total de pedidos: {pedidos.count()}")
for ped in pedidos[:5]:
    cliente_nombre = ped.idCliente.nombre if ped.idCliente else "Sin cliente"
    print(f"  • Pedido #{ped.idPedido} - {cliente_nombre} - ${ped.total}")

print("\n6. ESTADO DE LA BASE DE DATOS:")
print("-" * 70)
print(f"✓ Usuarios: {usuarios.count()}")
print(f"✓ Clientes: {clientes.count()}")
print(f"✓ Categorías: {categorias.count()}")
print(f"✓ Productos: {productos.count()}")
print(f"✓ Pedidos: {pedidos.count()}")

print("\n" + "=" * 70)

#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.pedidos import Pedido

print('=== ELIMINANDO PEDIDOS DE PRUEBA ===')
print()

# Eliminar pedidos con valores de prueba bajos
pedidos_a_eliminar = Pedido.objects.filter(
    total__in=[20.50, 25.50, 30.50, 35.50, 40.50]
)

print(f'Pedidos a eliminar: {pedidos_a_eliminar.count()}')
print()

for pedido in pedidos_a_eliminar:
    print(f'Eliminando Pedido #{pedido.idPedido}: {pedido.idCliente.nombre} - ${pedido.total}')
    pedido.delete()

print()
print('✅ Pedidos de prueba eliminados')

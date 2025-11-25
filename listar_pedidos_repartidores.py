#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.repartidores import Repartidor
from core.models.pedidos import Pedido

print('=== PEDIDOS POR REPARTIDOR ===')
print()

repartidores = Repartidor.objects.filter(email__isnull=False).exclude(email='')

for repartidor in repartidores:
    todos = Pedido.objects.filter(idRepartidor=repartidor, estado_pedido__in=['En Camino', 'Confirmado'])
    
    print(f'{repartidor.nombreRepartidor}:')
    print(f'  Total pedidos pendientes: {todos.count()}')
    
    for pedido in todos:
        print(f'    - Pedido #{pedido.idPedido}: {pedido.idCliente.nombre} - ${pedido.total}')
    print()

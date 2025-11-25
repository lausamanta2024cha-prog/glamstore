#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.utils import timezone
from core.models.pedidos import Pedido

print('Fecha actual:', timezone.now().date())
print()

pedidos = Pedido.objects.all()
for pedido in pedidos:
    print(f'Pedido #{pedido.idPedido}: {pedido.fechaCreacion.date()} - {pedido.idCliente.nombre} - ${pedido.total}')

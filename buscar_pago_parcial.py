#!/usr/bin/env python
"""
Script para buscar pedidos con pago parcial
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Pedido

def buscar_pedidos_pago_parcial():
    print("Buscando pedidos con estado 'Pago Parcial'...")
    
    pedidos_parciales = Pedido.objects.filter(estado='Pago Parcial')
    print(f"Pedidos con estado 'Pago Parcial': {pedidos_parciales.count()}")
    
    for pedido in pedidos_parciales:
        repartidor = pedido.idRepartidor.nombreRepartidor if pedido.idRepartidor else "Sin asignar"
        print(f"   Pedido #{pedido.idPedido}: Total ${pedido.total}, Repartidor: {repartidor}")

def buscar_todos_los_estados():
    print(f"\nTodos los estados de pedidos:")
    estados = Pedido.objects.values_list('estado', flat=True).distinct()
    for estado in estados:
        count = Pedido.objects.filter(estado=estado).count()
        print(f"   '{estado}': {count} pedidos")

if __name__ == "__main__":
    buscar_pedidos_pago_parcial()
    buscar_todos_los_estados()
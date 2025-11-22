#!/usr/bin/env python
"""
Script para crear pedidos de prueba con pago parcial
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Pedido, Cliente
from datetime import datetime

def crear_pedidos_pago_parcial():
    print("Creando pedidos de prueba con pago parcial...")
    
    # Buscar un cliente existente
    cliente = Cliente.objects.first()
    if not cliente:
        print("No hay clientes disponibles")
        return
    
    # Crear 2 pedidos de prueba con pago parcial
    for i in range(2):
        pedido = Pedido.objects.create(
            idCliente=cliente,
            estado='Pago Parcial',
            total=50000 + (i * 10000),  # $50,000 y $60,000
            fechaCreacion=datetime.now()
        )
        print(f"   Creado pedido #{pedido.idPedido} con estado 'Pago Parcial' y total ${pedido.total}")

def verificar_pedidos_creados():
    print(f"\nVerificando pedidos con pago parcial...")
    
    pedidos_parciales = Pedido.objects.filter(estado='Pago Parcial')
    print(f"Pedidos con estado 'Pago Parcial': {pedidos_parciales.count()}")
    
    for pedido in pedidos_parciales:
        estado_pago = pedido.get_estado_pago()
        print(f"   Pedido #{pedido.idPedido}:")
        print(f"      Estado BD: '{pedido.estado}'")
        print(f"      get_estado_pago(): {estado_pago}")
        print(f"      Total: ${pedido.total}")
        print(f"      PDF mostraría: {'PAGO PARCIAL - COBRAR $10,000' if estado_pago == 'Pago Parcial' else 'PAGO COMPLETO'}")

if __name__ == "__main__":
    crear_pedidos_pago_parcial()
    verificar_pedidos_creados()
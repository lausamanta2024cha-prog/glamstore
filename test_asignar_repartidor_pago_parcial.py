#!/usr/bin/env python
"""
Script para probar la asignación de repartidor a pedidos con pago parcial
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Pedido, Repartidor

def test_asignar_repartidor():
    print("Probando asignación de repartidor a pedido con pago parcial...")
    
    # Buscar un pedido con pago parcial
    pedido = Pedido.objects.filter(estado='Pago Parcial').first()
    if not pedido:
        print("No hay pedidos con pago parcial")
        return
    
    # Buscar un repartidor
    repartidor = Repartidor.objects.first()
    if not repartidor:
        print("No hay repartidores disponibles")
        return
    
    print(f"ANTES de asignar repartidor:")
    print(f"   Pedido #{pedido.idPedido}")
    print(f"   Estado: '{pedido.estado}'")
    print(f"   get_estado_pago(): {pedido.get_estado_pago()}")
    print(f"   Repartidor: {pedido.idRepartidor}")
    
    # Simular la lógica de asignación
    estado_original = pedido.estado
    pedido.idRepartidor = repartidor
    
    # Aplicar la lógica de preservación
    if estado_original == 'Pago Parcial':
        # Era pago parcial, NO cambiar el estado
        pass  # Mantener 'Pago Parcial'
    elif estado_original == 'Pago Completo':
        pedido.estado = 'En Camino'
    else:
        pedido.estado = 'En Camino'
    
    pedido.save()
    
    print(f"\nDESPUÉS de asignar repartidor:")
    print(f"   Pedido #{pedido.idPedido}")
    print(f"   Estado: '{pedido.estado}'")
    print(f"   get_estado_pago(): {pedido.get_estado_pago()}")
    print(f"   Repartidor: {pedido.idRepartidor.nombreRepartidor}")
    
    if pedido.get_estado_pago() == 'Pago Parcial':
        print(f"   ✅ PDF mostrará: PAGO PARCIAL - COBRAR $10,000")
    else:
        print(f"   ❌ PDF mostrará: PAGO COMPLETO")

if __name__ == "__main__":
    test_asignar_repartidor()
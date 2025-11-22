#!/usr/bin/env python
"""
Script para corregir automáticamente pedidos que deberían ser de pago parcial
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Pedido

def corregir_pedidos_automatico():
    print("Corrigiendo automáticamente pedidos que deberían ser de pago parcial...")
    
    # Buscar pedidos con totales que sugieren pago parcial
    pedidos = Pedido.objects.filter(estado='En Camino')
    pedidos_corregidos = 0
    
    for pedido in pedidos:
        total_float = float(pedido.total)
        
        # Si el total no es múltiplo de 10000, probablemente es pago parcial
        if total_float % 10000 != 0:
            print(f"   Corrigiendo Pedido #{pedido.idPedido}: ${pedido.total}")
            
            # Cambiar a pago parcial
            pedido.estado = 'Pago Parcial'
            pedido.save()
            pedidos_corregidos += 1
    
    print(f"\n✅ Pedidos corregidos: {pedidos_corregidos}")
    
    # Verificar resultado
    pedidos_parciales = Pedido.objects.filter(estado='Pago Parcial')
    print(f"Total de pedidos con 'Pago Parcial': {pedidos_parciales.count()}")

if __name__ == "__main__":
    corregir_pedidos_automatico()
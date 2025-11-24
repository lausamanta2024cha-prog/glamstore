#!/usr/bin/env python
"""
Script para corregir los totales de los pedidos existentes.
Recalcula el total incluyendo IVA (19%) y envío según corresponda.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Pedido, DetallePedido
from decimal import Decimal

def corregir_totales():
    """Recalcula y corrige los totales de todos los pedidos."""
    pedidos = Pedido.objects.all()
    costo_envio = 10000
    tasa_iva = Decimal('0.19')
    
    pedidos_corregidos = 0
    
    for pedido in pedidos:
        # Obtener detalles del pedido
        detalles = DetallePedido.objects.filter(idPedido=pedido)
        
        # Calcular base líquida
        total_productos = sum(detalle.subtotal for detalle in detalles)
        
        # Calcular IVA
        iva = int(total_productos * tasa_iva)
        
        # Calcular total según estado de pago
        if pedido.estado_pago == 'Pago Completo':
            total_correcto = int(total_productos + iva + costo_envio)
        else:  # Pago Parcial
            total_correcto = int(total_productos + iva)
        
        # Si el total es diferente, actualizar
        if int(pedido.total) != total_correcto:
            print(f"Pedido #{pedido.idPedido}:")
            print(f"  Total anterior: ${pedido.total}")
            print(f"  Base líquida: ${total_productos}")
            print(f"  IVA (19%): ${iva}")
            print(f"  Envío: ${costo_envio if pedido.estado_pago == 'Pago Completo' else 0}")
            print(f"  Total correcto: ${total_correcto}")
            
            pedido.total = total_correcto
            pedido.save()
            pedidos_corregidos += 1
            print(f"  ✓ Corregido\n")
        else:
            print(f"Pedido #{pedido.idPedido}: Total correcto (${pedido.total})")
    
    print(f"\n{'='*50}")
    print(f"Total de pedidos corregidos: {pedidos_corregidos}")
    print(f"Total de pedidos procesados: {pedidos.count()}")

if __name__ == '__main__':
    corregir_totales()

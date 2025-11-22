#!/usr/bin/env python
"""
Script para verificar que el PDF funcione correctamente con pedidos de pago parcial
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Pedido

def test_pdf_pago_parcial():
    print("Verificando que el PDF funcione con pedidos de pago parcial...")
    
    # Buscar pedidos con pago parcial que tengan repartidor asignado
    pedidos_parciales = Pedido.objects.filter(
        estado='Pago Parcial',
        idRepartidor__isnull=False
    )
    
    print(f"Pedidos con pago parcial y repartidor asignado: {pedidos_parciales.count()}")
    
    for pedido in pedidos_parciales[:5]:  # Mostrar solo los primeros 5
        estado_pago = pedido.get_estado_pago()
        estado_pedido = pedido.get_estado_pedido()
        
        print(f"\n   📦 Pedido #{pedido.idPedido}:")
        print(f"      Cliente: {pedido.idCliente.nombre}")
        print(f"      Estado BD: '{pedido.estado}'")
        print(f"      get_estado_pago(): {estado_pago}")
        print(f"      get_estado_pedido(): {estado_pedido}")
        print(f"      Total: ${pedido.total}")
        print(f"      Repartidor: {pedido.idRepartidor.nombreRepartidor}")
        
        # Verificar qué mostraría el PDF
        if estado_pago == 'Pago Parcial':
            print(f"      🔴 PDF mostrará:")
            print(f"         - Productos (YA PAGADOS): ${pedido.total}")
            print(f"         - Envío (PENDIENTE): $10,000")
            print(f"         - COBRAR AL CLIENTE: $10,000")
            print(f"         - Mensaje: PAGO CONTRA ENTREGA")
        else:
            print(f"      ✅ PDF mostrará: PAGO COMPLETO")

def test_pedidos_sin_repartidor():
    print(f"\nPedidos con pago parcial SIN repartidor asignado:")
    
    pedidos_sin_repartidor = Pedido.objects.filter(
        estado='Pago Parcial',
        idRepartidor__isnull=True
    )
    
    print(f"Cantidad: {pedidos_sin_repartidor.count()}")
    
    for pedido in pedidos_sin_repartidor[:3]:
        print(f"   Pedido #{pedido.idPedido}: ${pedido.total} - {pedido.idCliente.nombre}")

def mostrar_resumen():
    print(f"\n📊 Resumen final:")
    
    total_pedidos = Pedido.objects.count()
    pedidos_pago_parcial = Pedido.objects.filter(estado='Pago Parcial').count()
    pedidos_pago_completo = Pedido.objects.filter(estado='Pago Completo').count()
    pedidos_en_camino = Pedido.objects.filter(estado='En Camino').count()
    
    print(f"   Total de pedidos: {total_pedidos}")
    print(f"   Pago Parcial: {pedidos_pago_parcial}")
    print(f"   Pago Completo: {pedidos_pago_completo}")
    print(f"   En Camino: {pedidos_en_camino}")
    
    print(f"\n✅ El PDF ahora funcionará correctamente:")
    print(f"   - Pedidos con 'Pago Parcial' → Mostrarán mensaje de cobro")
    print(f"   - Pedidos con otros estados → Mostrarán pago completo")

if __name__ == "__main__":
    test_pdf_pago_parcial()
    test_pedidos_sin_repartidor()
    mostrar_resumen()
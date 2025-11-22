#!/usr/bin/env python
"""
Script para verificar qué pedidos deberían ser de pago parcial
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Pedido

def verificar_pedidos_actuales():
    print("Verificando pedidos actuales...")
    
    # Obtener todos los pedidos
    pedidos = Pedido.objects.all().order_by('-idPedido')[:10]
    
    print(f"\nÚltimos 10 pedidos:")
    for pedido in pedidos:
        estado_pago = pedido.get_estado_pago()
        estado_pedido = pedido.get_estado_pedido()
        
        print(f"\n   Pedido #{pedido.idPedido}:")
        print(f"      Estado en BD: '{pedido.estado}'")
        print(f"      Estado de pago detectado: {estado_pago}")
        print(f"      Estado de pedido: {estado_pedido}")
        print(f"      Total: ${pedido.total}")
        print(f"      Cliente: {pedido.idCliente.nombre}")
        print(f"      Repartidor: {pedido.idRepartidor.nombreRepartidor if pedido.idRepartidor else 'Sin asignar'}")
        
        # Verificar si el PDF mostraría pago parcial
        if estado_pago == 'Pago Parcial':
            print(f"      PDF: PAGO PARCIAL - COBRAR $10,000")
        else:
            print(f"      PDF: PAGO COMPLETO")

def verificar_metodo_get_estado_pago():
    print(f"\nVerificando método get_estado_pago()...")
    
    # Probar con diferentes estados
    estados_prueba = [
        "Pago Parcial",
        "Pago Completo", 
        "En Camino",
        "Entregado",
        "Completado"
    ]
    
    for estado in estados_prueba:
        # Simular pedido con este estado
        class PedidoTest:
            def __init__(self, estado):
                self.estado = estado
            
            def get_estado_pago(self):
                if self.estado == 'Pago Parcial':
                    return 'Pago Parcial'
                elif self.estado in ['Entregado', 'Completado']:
                    return 'Pago Completo'
                else:
                    return 'Pago Completo'
        
        pedido_test = PedidoTest(estado)
        resultado = pedido_test.get_estado_pago()
        
        print(f"   Estado '{estado}' → get_estado_pago(): {resultado}")

def buscar_pedidos_que_deberian_ser_parciales():
    print(f"\nBuscando pedidos que deberían ser de pago parcial...")
    
    # Buscar pedidos con estados que podrían indicar pago parcial
    pedidos_sospechosos = Pedido.objects.filter(estado__in=['En Camino', 'Entregado', 'Completado'])
    
    print(f"Pedidos con estados 'En Camino', 'Entregado', 'Completado': {pedidos_sospechosos.count()}")
    
    for pedido in pedidos_sospechosos[:5]:
        print(f"\n   Pedido #{pedido.idPedido}:")
        print(f"      Estado: '{pedido.estado}'")
        print(f"      Total: ${pedido.total}")
        print(f"      Fecha: {pedido.fechaCreacion}")
        
        # Si el total es "redondo" sin envío, podría ser pago parcial
        total_float = float(pedido.total)
        if total_float % 10000 != 0:  # No es múltiplo de 10000
            print(f"      POSIBLE PAGO PARCIAL (total no incluye envío)")
        else:
            print(f"      Posiblemente pago completo")

if __name__ == "__main__":
    verificar_pedidos_actuales()
    verificar_metodo_get_estado_pago()
    buscar_pedidos_que_deberian_ser_parciales()
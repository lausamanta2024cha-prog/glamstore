#!/usr/bin/env python
"""
Script para corregir pedidos existentes que deberían ser de pago parcial
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Pedido

def identificar_pedidos_a_corregir():
    print("Identificando pedidos que deberían ser de pago parcial...")
    
    # Buscar pedidos con totales que sugieren pago parcial
    # (totales que no son múltiplos de 10000, sugiriendo que no incluyen envío)
    pedidos_candidatos = []
    
    pedidos = Pedido.objects.filter(estado='En Camino')
    
    for pedido in pedidos:
        total_float = float(pedido.total)
        
        # Si el total no es múltiplo de 10000, probablemente es pago parcial
        if total_float % 10000 != 0:
            pedidos_candidatos.append(pedido)
    
    print(f"Pedidos candidatos a ser pago parcial: {len(pedidos_candidatos)}")
    
    for pedido in pedidos_candidatos[:10]:  # Mostrar solo los primeros 10
        print(f"   Pedido #{pedido.idPedido}: ${pedido.total} - {pedido.idCliente.nombre}")
    
    return pedidos_candidatos

def corregir_pedidos_seleccionados():
    print(f"\nCorrigiendo pedidos específicos que sabemos son de pago parcial...")
    
    # Lista de pedidos que sabemos que deberían ser pago parcial
    # (puedes agregar más IDs aquí basándote en tu conocimiento)
    pedidos_a_corregir = [48, 47, 46, 45, 44]  # Ejemplos
    
    for pedido_id in pedidos_a_corregir:
        try:
            pedido = Pedido.objects.get(idPedido=pedido_id)
            
            print(f"   Pedido #{pedido_id}:")
            print(f"      Estado actual: '{pedido.estado}'")
            print(f"      Total: ${pedido.total}")
            
            # Cambiar a pago parcial
            pedido.estado = 'Pago Parcial'
            pedido.save()
            
            print(f"      ✅ Corregido a: '{pedido.estado}'")
            print(f"      PDF ahora mostrará: PAGO PARCIAL - COBRAR $10,000")
            
        except Pedido.DoesNotExist:
            print(f"   ❌ Pedido #{pedido_id} no encontrado")

def verificar_correccion():
    print(f"\nVerificando corrección...")
    
    pedidos_parciales = Pedido.objects.filter(estado='Pago Parcial')
    print(f"Total de pedidos con 'Pago Parcial': {pedidos_parciales.count()}")
    
    for pedido in pedidos_parciales:
        repartidor = pedido.idRepartidor.nombreRepartidor if pedido.idRepartidor else "Sin asignar"
        print(f"   Pedido #{pedido.idPedido}: ${pedido.total}, Repartidor: {repartidor}")

def mostrar_instrucciones():
    print(f"\n📝 Instrucciones para el futuro:")
    print(f"   1. Los nuevos pedidos con 'Pago Parcial' se crearán correctamente")
    print(f"   2. Al asignar repartidor, el estado se preservará como 'Pago Parcial'")
    print(f"   3. El PDF mostrará automáticamente el mensaje de cobro")
    print(f"   4. Para pedidos existentes, usa este script para corregirlos manualmente")

if __name__ == "__main__":
    candidatos = identificar_pedidos_a_corregir()
    
    respuesta = input(f"\n¿Quieres corregir algunos pedidos específicos? (s/n): ")
    if respuesta.lower() == 's':
        corregir_pedidos_seleccionados()
        verificar_correccion()
    
    mostrar_instrucciones()
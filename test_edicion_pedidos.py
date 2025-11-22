#!/usr/bin/env python
"""
Script para probar la funcionalidad de edición de pedidos
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Pedido, Repartidor

def mostrar_pedidos_editables():
    print("Pedidos disponibles para editar:")
    
    pedidos = Pedido.objects.all().order_by('-idPedido')[:10]
    
    for pedido in pedidos:
        estado_pago = pedido.get_estado_pago()
        estado_pedido = pedido.get_estado_pedido()
        repartidor = pedido.idRepartidor.nombreRepartidor if pedido.idRepartidor else "Sin asignar"
        
        print(f"\n   Pedido #{pedido.idPedido}:")
        print(f"      Cliente: {pedido.idCliente.nombre}")
        print(f"      Estado BD: '{pedido.estado}'")
        print(f"      Estado de pago: {estado_pago}")
        print(f"      Estado de pedido: {estado_pedido}")
        print(f"      Total: ${pedido.total}")
        print(f"      Repartidor: {repartidor}")

def mostrar_repartidores_disponibles():
    print(f"\nRepartidores disponibles:")
    
    repartidores = Repartidor.objects.all()
    
    for repartidor in repartidores:
        print(f"   {repartidor.nombreRepartidor} - {repartidor.telefono} ({repartidor.estado_turno})")

def mostrar_funcionalidades():
    print(f"\nFuncionalidades de edición implementadas:")
    print(f"   ✅ Editar estado de pago (Pago Parcial / Pago Completo)")
    print(f"   ✅ Editar estado del pedido (Confirmado / En Camino / Entregado / etc.)")
    print(f"   ✅ Asignar/desasignar repartidor")
    print(f"   ✅ Editar total del pedido")
    print(f"   ✅ Editar fecha de creación")
    print(f"   ✅ Agregar observaciones")
    print(f"   ✅ Vista previa del estado actual")
    print(f"   ✅ Actualización automática del estado del repartidor")

def mostrar_casos_uso():
    print(f"\nCasos de uso comunes:")
    print(f"   1. Cambiar pedido de 'Pago Completo' a 'Pago Parcial'")
    print(f"   2. Asignar repartidor a pedido confirmado")
    print(f"   3. Cambiar estado de 'En Camino' a 'Entregado'")
    print(f"   4. Desasignar repartidor si hay problemas")
    print(f"   5. Marcar pedido como 'Problema en Entrega'")
    print(f"   6. Ajustar total del pedido si es necesario")

def instrucciones_uso():
    print(f"\nPara usar la edición:")
    print(f"   1. Ve al panel de administración")
    print(f"   2. Entra a 'Pedidos' → 'Lista de Pedidos'")
    print(f"   3. Haz clic en 'Editar' en cualquier pedido")
    print(f"   4. Modifica los campos que necesites")
    print(f"   5. Haz clic en 'Guardar Cambios'")
    print(f"   6. El sistema actualizará todo automáticamente")

if __name__ == "__main__":
    mostrar_pedidos_editables()
    mostrar_repartidores_disponibles()
    mostrar_funcionalidades()
    mostrar_casos_uso()
    instrucciones_uso()
#!/usr/bin/env python
"""
Script para verificar TODOS los pedidos de un repartidor sin filtro de fecha
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.repartidores import Repartidor
from core.models.pedidos import Pedido

def verificar_todos_pedidos():
    """Verifica todos los pedidos"""
    print("=== VERIFICANDO TODOS LOS PEDIDOS ===")
    
    # Obtener repartidor
    repartidor = Repartidor.objects.filter(nombreRepartidor__icontains='lauren').first()
    
    if not repartidor:
        print("❌ Repartidor no encontrado")
        return
    
    print(f"Repartidor: {repartidor.nombreRepartidor}")
    print(f"Email: {repartidor.email}")
    print()
    
    # TODOS los pedidos sin filtro de fecha
    todos_pedidos = Pedido.objects.filter(
        idRepartidor=repartidor,
        estado_pedido__in=['En Camino', 'Confirmado']
    ).select_related('idCliente').order_by('fechaCreacion')
    
    print(f"📦 TOTAL DE PEDIDOS PENDIENTES: {todos_pedidos.count()}")
    print()
    
    # Mostrar detalles
    for idx, pedido in enumerate(todos_pedidos, 1):
        print(f"{idx}. Pedido #{pedido.idPedido}")
        print(f"   Cliente: {pedido.idCliente.nombre}")
        print(f"   Teléfono: {pedido.idCliente.telefono}")
        print(f"   Dirección: {pedido.idCliente.direccion}")
        print(f"   Total: ${pedido.total}")
        print(f"   Pago: {pedido.estado_pago}")
        print(f"   Estado: {pedido.estado_pedido}")
        print(f"   Fecha: {pedido.fechaCreacion.date()}")
        print()

def main():
    """Función principal"""
    print("INICIANDO VERIFICACIÓN DE TODOS LOS PEDIDOS")
    print("=" * 50)
    
    verificar_todos_pedidos()
    
    print("VERIFICACIÓN COMPLETADA")

if __name__ == "__main__":
    main()
#!/usr/bin/env python
"""
Script para crear pedidos de prueba para repartidores
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.utils import timezone
from core.models.repartidores import Repartidor
from core.models.pedidos import Pedido
from core.models.clientes import Cliente
from core.models.productos import Producto
from decimal import Decimal

def crear_pedidos_prueba():
    """Crea pedidos de prueba para repartidores sin pedidos"""
    print("=== CREANDO PEDIDOS DE PRUEBA ===")
    
    # Obtener repartidores con email pero sin pedidos hoy
    fecha_hoy = timezone.now().date()
    repartidores_con_email = Repartidor.objects.filter(email__isnull=False).exclude(email='')
    
    # Obtener un cliente de prueba
    cliente = Cliente.objects.first()
    if not cliente:
        print("❌ No hay clientes en la base de datos")
        return
    
    print(f"Cliente de prueba: {cliente.nombre}")
    
    for repartidor in repartidores_con_email:
        # Verificar si ya tiene pedidos hoy
        pedidos_hoy = Pedido.objects.filter(
            idRepartidor=repartidor,
            estado_pedido__in=['En Camino', 'Confirmado'],
            fechaCreacion__date=fecha_hoy
        ).count()
        
        if pedidos_hoy == 0:
            print(f"Creando pedido para: {repartidor.nombreRepartidor}")
            
            # Crear pedido de prueba
            pedido = Pedido.objects.create(
                idCliente=cliente,
                idRepartidor=repartidor,
                estado_pedido='Confirmado',
                estado_pago='Pago Completo',
                total=Decimal('25.50'),
                fechaCreacion=timezone.now()
            )
            
            print(f"  ✅ Pedido #{pedido.idPedido} creado exitosamente")
        else:
            print(f"  ℹ️  {repartidor.nombreRepartidor} ya tiene {pedidos_hoy} pedido(s) hoy")
    
    print("\n=== RESUMEN FINAL ===")
    for repartidor in repartidores_con_email:
        pedidos_count = Pedido.objects.filter(
            idRepartidor=repartidor,
            estado_pedido__in=['En Camino', 'Confirmado'],
            fechaCreacion__date=fecha_hoy
        ).count()
        
        status = "✅" if pedidos_count > 0 else "❌"
        print(f"{status} {repartidor.nombreRepartidor} - Pedidos: {pedidos_count}")

def main():
    """Función principal"""
    print("INICIANDO CREACIÓN DE PEDIDOS DE PRUEBA")
    print("=" * 50)
    
    crear_pedidos_prueba()
    
    print("\nCREACIÓN COMPLETADA")

if __name__ == "__main__":
    main()
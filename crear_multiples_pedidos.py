#!/usr/bin/env python
"""
Script para crear múltiples pedidos para un repartidor específico
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.utils import timezone
from core.models.repartidores import Repartidor
from core.models.pedidos import Pedido, DetallePedido
from core.models.clientes import Cliente
from core.models.productos import Producto
from decimal import Decimal

def crear_multiples_pedidos():
    """Crea múltiples pedidos para un repartidor"""
    print("=== CREANDO MÚLTIPLES PEDIDOS PARA PRUEBA ===")
    
    # Obtener el primer repartidor con email
    repartidor = Repartidor.objects.filter(email__isnull=False).exclude(email='').first()
    if not repartidor:
        print("❌ No hay repartidores con email")
        return
    
    print(f"Repartidor seleccionado: {repartidor.nombreRepartidor} ({repartidor.email})")
    
    # Obtener clientes
    clientes = Cliente.objects.all()[:3]  # Usar hasta 3 clientes diferentes
    if not clientes:
        print("❌ No hay clientes en la base de datos")
        return
    
    # Obtener productos
    productos = Producto.objects.all()[:5]  # Usar hasta 5 productos
    if not productos:
        print("❌ No hay productos en la base de datos")
        return
    
    fecha_hoy = timezone.now()
    
    # Crear 5 pedidos para el mismo repartidor
    for i in range(5):
        cliente = clientes[i % len(clientes)]  # Rotar entre clientes
        
        pedido = Pedido.objects.create(
            idCliente=cliente,
            idRepartidor=repartidor,
            estado_pedido='Confirmado',
            estado_pago='Pago Completo',
            total=Decimal(f'{20 + (i * 5)}.50'),  # Totales diferentes
            fechaCreacion=fecha_hoy
        )
        
        # Agregar algunos productos al pedido
        for j in range(min(2, len(productos))):  # 2 productos por pedido
            producto = productos[j]
            cantidad = j + 1
            precio_unitario = Decimal(f'{10 + j}.00')
            subtotal = precio_unitario * cantidad
            
            DetallePedido.objects.create(
                idPedido=pedido,
                idProducto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal
            )
        
        print(f"  ✅ Pedido #{pedido.idPedido} creado - Cliente: {cliente.nombre} - Total: ${pedido.total}")
    
    # Mostrar resumen
    pedidos_total = Pedido.objects.filter(
        idRepartidor=repartidor,
        estado_pedido__in=['En Camino', 'Confirmado'],
        fechaCreacion__date=fecha_hoy.date()
    ).count()
    
    print(f"\n📊 Total de pedidos para {repartidor.nombreRepartidor} hoy: {pedidos_total}")

def main():
    """Función principal"""
    print("INICIANDO CREACIÓN DE MÚLTIPLES PEDIDOS")
    print("=" * 50)
    
    crear_multiples_pedidos()
    
    print("\nCREACIÓN COMPLETADA")

if __name__ == "__main__":
    main()
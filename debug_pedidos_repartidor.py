#!/usr/bin/env python
"""
Script para debuggear los pedidos de un repartidor específico
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
from core.Gestion_admin.services_repartidores import enviar_correo_repartidor_detallado

def debug_pedidos_repartidor():
    """Debug de pedidos de un repartidor específico"""
    print("=== DEBUG PEDIDOS REPARTIDOR ===")
    
    # Obtener el repartidor con más pedidos
    repartidor = Repartidor.objects.filter(email__isnull=False).exclude(email='').first()
    if not repartidor:
        print("❌ No hay repartidores con email")
        return
    
    fecha_hoy = timezone.now().date()
    
    print(f"Repartidor: {repartidor.nombreRepartidor} ({repartidor.email})")
    print(f"Fecha: {fecha_hoy}")
    print()
    
    # Obtener pedidos del repartidor
    pedidos = Pedido.objects.filter(
        idRepartidor=repartidor,
        estado_pedido__in=['En Camino', 'Confirmado'],
        fechaCreacion__date=fecha_hoy
    ).select_related('idCliente').prefetch_related('detallepedido_set__idProducto')
    
    print(f"📦 Total de pedidos encontrados: {pedidos.count()}")
    print()
    
    # Mostrar detalles de cada pedido
    for idx, pedido in enumerate(pedidos, 1):
        print(f"Pedido #{idx}:")
        print(f"  ID: {pedido.idPedido}")
        print(f"  Cliente: {pedido.idCliente.nombre}")
        print(f"  Teléfono: {pedido.idCliente.telefono}")
        print(f"  Dirección: {pedido.idCliente.direccion}")
        print(f"  Total: ${pedido.total}")
        print(f"  Estado: {pedido.estado_pedido}")
        print(f"  Fecha: {pedido.fechaCreacion}")
        
        # Mostrar productos del pedido
        detalles = pedido.detallepedido_set.all()
        print(f"  Productos ({detalles.count()}):")
        for detalle in detalles:
            print(f"    - {detalle.idProducto.nombreProducto}: {detalle.cantidad} x ${detalle.precio_unitario}")
        print()
    
    # Probar envío de correo
    print("🔄 Probando envío de correo...")
    resultado = enviar_correo_repartidor_detallado(repartidor, fecha_hoy)
    
    if resultado:
        print("✅ Correo enviado exitosamente")
    else:
        print("❌ Error al enviar correo")

def main():
    """Función principal"""
    print("INICIANDO DEBUG DE PEDIDOS")
    print("=" * 50)
    
    debug_pedidos_repartidor()
    
    print("\nDEBUG COMPLETADO")

if __name__ == "__main__":
    main()
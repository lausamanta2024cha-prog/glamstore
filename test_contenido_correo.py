#!/usr/bin/env python
"""
Script para verificar el contenido del correo que se envía
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
from datetime import timedelta

def verificar_contenido_correo():
    """Verifica el contenido del correo"""
    print("=== VERIFICANDO CONTENIDO DEL CORREO ===")
    
    # Obtener un repartidor con email y pedidos
    repartidor = Repartidor.objects.filter(email__isnull=False).exclude(email='').first()
    
    if not repartidor:
        print("❌ No hay repartidores con email")
        return
    
    fecha = timezone.now().date()
    fecha_manana = fecha + timedelta(days=1)
    
    print(f"Repartidor: {repartidor.nombreRepartidor}")
    print(f"Email: {repartidor.email}")
    print()
    
    # Obtener pedidos
    pedidos_hoy = Pedido.objects.filter(
        idRepartidor=repartidor,
        estado_pedido__in=['En Camino', 'Confirmado'],
        fechaCreacion__date=fecha
    ).select_related('idCliente').prefetch_related('detallepedido_set__idProducto')
    
    pedidos_manana = Pedido.objects.filter(
        idRepartidor=repartidor,
        estado_pedido__in=['En Camino', 'Confirmado'],
        fechaCreacion__date=fecha_manana
    ).select_related('idCliente').prefetch_related('detallepedido_set__idProducto')
    
    print(f"📦 Pedidos hoy: {pedidos_hoy.count()}")
    print(f"📦 Pedidos mañana: {pedidos_manana.count()}")
    print()
    
    # Mostrar detalles de cada pedido
    print("=== PEDIDOS DE HOY ===")
    for idx, pedido in enumerate(pedidos_hoy, 1):
        es_soacha = 'soacha' in pedido.idCliente.direccion.lower()
        print(f"\n{idx}. {pedido.idCliente.nombre}")
        print(f"   Teléfono: {pedido.idCliente.telefono}")
        print(f"   Dirección: {pedido.idCliente.direccion}")
        print(f"   Total: ${pedido.total}")
        print(f"   Pago: {pedido.estado_pago}")
        print(f"   Soacha: {'Sí' if es_soacha else 'No'}")
        print(f"   Productos: {pedido.detallepedido_set.count()}")
        
        # Mostrar productos
        for detalle in pedido.detallepedido_set.all():
            print(f"      - {detalle.idProducto.nombreProducto}: {detalle.cantidad} x ${detalle.precio_unitario}")
    
    print("\n=== PEDIDOS DE MAÑANA ===")
    for idx, pedido in enumerate(pedidos_manana, 1):
        es_soacha = 'soacha' in pedido.idCliente.direccion.lower()
        print(f"\n{idx}. {pedido.idCliente.nombre}")
        print(f"   Teléfono: {pedido.idCliente.telefono}")
        print(f"   Dirección: {pedido.idCliente.direccion}")
        print(f"   Total: ${pedido.total}")
        print(f"   Pago: {pedido.estado_pago}")
        print(f"   Soacha: {'Sí' if es_soacha else 'No'}")
        print(f"   Productos: {pedido.detallepedido_set.count()}")
        
        # Mostrar productos
        for detalle in pedido.detallepedido_set.all():
            print(f"      - {detalle.idProducto.nombreProducto}: {detalle.cantidad} x ${detalle.precio_unitario}")
    
    # Enviar correo
    print("\n" + "=" * 50)
    print("🔄 Enviando correo...")
    print("=" * 50)
    
    resultado = enviar_correo_repartidor_detallado(repartidor, fecha)
    
    if resultado:
        print("\n✅ Correo enviado exitosamente")
        print(f"Verifica tu email en: {repartidor.email}")
    else:
        print("\n❌ Error al enviar correo")

def main():
    """Función principal"""
    print("INICIANDO VERIFICACIÓN DE CONTENIDO DEL CORREO")
    print("=" * 50)
    
    verificar_contenido_correo()
    
    print("\nVERIFICACIÓN COMPLETADA")

if __name__ == "__main__":
    main()
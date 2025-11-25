#!/usr/bin/env python
"""
Script para calcular y guardar fechas de vencimiento para pedidos existentes
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.pedidos import Pedido
from core.Gestion_admin.services_repartidores import calcular_fecha_vencimiento
from datetime import timedelta

print('=== CALCULANDO FECHAS DE VENCIMIENTO ===')
print()

# Obtener todos los pedidos sin fecha de vencimiento
pedidos = Pedido.objects.filter(fecha_vencimiento__isnull=True)

print(f'Pedidos a procesar: {pedidos.count()}')
print()

actualizados = 0
for pedido in pedidos:
    try:
        # Determinar ciudad
        ciudad = 'Soacha' if pedido.idCliente.direccion and 'soacha' in pedido.idCliente.direccion.lower() else 'Bogotá'
        
        # Calcular fecha de vencimiento
        fecha_vencimiento = calcular_fecha_vencimiento(pedido.fechaCreacion.date(), ciudad)
        
        # Guardar
        pedido.fecha_vencimiento = fecha_vencimiento
        pedido.save()
        
        actualizados += 1
        
        if actualizados % 10 == 0:
            print(f'✓ {actualizados} pedidos procesados...')
    
    except Exception as e:
        print(f'❌ Error en pedido #{pedido.idPedido}: {str(e)}')

print()
print(f'✅ {actualizados} pedidos actualizados con fecha de vencimiento')

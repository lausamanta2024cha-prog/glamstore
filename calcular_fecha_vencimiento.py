#!/usr/bin/env python
"""
Script para calcular fecha de vencimiento de pedidos según ciudad
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.pedidos import Pedido
from datetime import timedelta, datetime

def es_dia_habil(fecha):
    """Verifica si es día hábil (lunes a viernes)"""
    return fecha.weekday() < 5  # 0-4 son lunes a viernes

def calcular_fecha_vencimiento(fecha_pedido, ciudad):
    """Calcula fecha de vencimiento según ciudad"""
    dias_vencimiento = 2 if 'bogota' in ciudad.lower() else 3
    
    fecha_actual = fecha_pedido
    dias_contados = 0
    
    while dias_contados < dias_vencimiento:
        fecha_actual += timedelta(days=1)
        if es_dia_habil(fecha_actual):
            dias_contados += 1
    
    return fecha_actual

print('=== CÁLCULO DE FECHA DE VENCIMIENTO ===')
print()

# Obtener pedidos con estado En Camino o Confirmado
pedidos = Pedido.objects.filter(
    estado_pedido__in=['En Camino', 'Confirmado']
).select_related('idCliente', 'idRepartidor')

for pedido in pedidos:
    fecha_pedido = pedido.fechaCreacion.date()
    
    # Determinar ciudad (por ahora asumimos Bogotá si no dice Soacha)
    ciudad = 'Bogotá'
    if pedido.idCliente.direccion and 'soacha' in pedido.idCliente.direccion.lower():
        ciudad = 'Soacha'
    
    fecha_vencimiento = calcular_fecha_vencimiento(fecha_pedido, ciudad)
    
    print(f'Pedido #{pedido.idPedido}:')
    print(f'  Cliente: {pedido.idCliente.nombre}')
    print(f'  Repartidor: {pedido.idRepartidor.nombreRepartidor if pedido.idRepartidor else "Sin asignar"}')
    print(f'  Fecha pedido: {fecha_pedido}')
    print(f'  Ciudad: {ciudad}')
    print(f'  Fecha vencimiento: {fecha_vencimiento}')
    print(f'  Total: ${pedido.total}')
    print(f'  Estado pago: {pedido.estado_pago}')
    print()

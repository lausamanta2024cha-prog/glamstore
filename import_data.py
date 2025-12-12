#!/usr/bin/env python
"""
Script para importar datos de repartidores y notificaciones desde JSON
"""
import os
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.repartidores import Repartidor
from core.models.notificaciones import NotificacionProblema
from core.models.pedidos import Pedido

def import_repartidores():
    """Importar repartidores desde JSON"""
    try:
        with open('repartidores_export.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for item in data:
            # Extraer el ID si existe
            repartidor_id = item.get('idRepartidor')
            
            # Crear o actualizar
            repartidor, created = Repartidor.objects.update_or_create(
                idRepartidor=repartidor_id,
                defaults={
                    'nombreRepartidor': item.get('nombreRepartidor'),
                    'telefono': item.get('telefono'),
                    'email': item.get('email'),
                }
            )
            count += 1
        
        print(f"✓ Importados {count} repartidores")
    except FileNotFoundError:
        print("✗ Archivo repartidores_export.json no encontrado")
    except Exception as e:
        print(f"✗ Error importando repartidores: {e}")

def import_notificaciones():
    """Importar notificaciones desde JSON"""
    try:
        with open('notificaciones_export.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for item in data:
            try:
                # Obtener el pedido
                pedido_id = item.get('idPedido')
                pedido = Pedido.objects.get(idPedido=pedido_id)
                
                # Convertir strings a datetime si es necesario
                fecha_reporte = item.get('fechaReporte')
                if isinstance(fecha_reporte, str):
                    fecha_reporte = datetime.fromisoformat(fecha_reporte)
                
                fecha_respuesta = item.get('fecha_respuesta')
                if fecha_respuesta and isinstance(fecha_respuesta, str):
                    fecha_respuesta = datetime.fromisoformat(fecha_respuesta)
                
                # Crear o actualizar
                notificacion, created = NotificacionProblema.objects.update_or_create(
                    idNotificacion=item.get('idNotificacion'),
                    defaults={
                        'idPedido': pedido,
                        'motivo': item.get('motivo'),
                        'foto': item.get('foto'),
                        'fechaReporte': fecha_reporte,
                        'leida': item.get('leida', False),
                        'respuesta_admin': item.get('respuesta_admin'),
                        'fecha_respuesta': fecha_respuesta,
                    }
                )
                count += 1
            except Pedido.DoesNotExist:
                print(f"  ⚠ Pedido {pedido_id} no encontrado, saltando notificación")
            except Exception as e:
                print(f"  ⚠ Error importando notificación: {e}")
        
        print(f"✓ Importadas {count} notificaciones")
    except FileNotFoundError:
        print("✗ Archivo notificaciones_export.json no encontrado")
    except Exception as e:
        print(f"✗ Error importando notificaciones: {e}")

if __name__ == '__main__':
    print("Importando datos...")
    import_repartidores()
    import_notificaciones()
    print("\n✓ Importación completada")

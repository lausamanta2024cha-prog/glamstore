"""
Comando Django para importar repartidores y notificaciones desde JSON
Uso: python manage.py import_data
"""
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from core.models.repartidores import Repartidor
from core.models.notificaciones import NotificacionProblema
from core.models.pedidos import Pedido


class Command(BaseCommand):
    help = 'Importa repartidores y notificaciones desde archivos JSON'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Importando datos...'))
        
        # Importar repartidores
        self.import_repartidores()
        
        # Importar notificaciones
        self.import_notificaciones()
        
        self.stdout.write(self.style.SUCCESS('\n✓ Importación completada'))

    def import_repartidores(self):
        """Importar repartidores desde JSON"""
        try:
            with open('repartidores_export.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            count = 0
            for item in data:
                try:
                    repartidor, created = Repartidor.objects.update_or_create(
                        idRepartidor=item.get('idRepartidor'),
                        defaults={
                            'nombreRepartidor': item.get('nombreRepartidor'),
                            'telefono': item.get('telefono'),
                            'email': item.get('email'),
                        }
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'  ⚠ Error importando repartidor {item.get("idRepartidor")}: {e}'
                    ))
            
            self.stdout.write(self.style.SUCCESS(f'✓ Importados {count} repartidores'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                '✗ Archivo repartidores_export.json no encontrado'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error importando repartidores: {e}'))

    def import_notificaciones(self):
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
                    self.stdout.write(self.style.WARNING(
                        f'  ⚠ Pedido {pedido_id} no encontrado, saltando notificación'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'  ⚠ Error importando notificación: {e}'
                    ))
            
            self.stdout.write(self.style.SUCCESS(f'✓ Importadas {count} notificaciones'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                '✗ Archivo notificaciones_export.json no encontrado'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error importando notificaciones: {e}'))

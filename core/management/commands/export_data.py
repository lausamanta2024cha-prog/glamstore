"""
Comando Django para exportar repartidores y notificaciones a JSON
Uso: python manage.py export_data
"""
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from core.models.repartidores import Repartidor
from core.models.notificaciones import NotificacionProblema


class Command(BaseCommand):
    help = 'Exporta repartidores y notificaciones a archivos JSON'

    def serialize_datetime(self, obj):
        """Serializar datetime a string ISO"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Exportando datos...'))
        
        # Exportar repartidores
        try:
            repartidores = list(Repartidor.objects.all().values())
            with open('repartidores_export.json', 'w', encoding='utf-8') as f:
                json.dump(repartidores, f, indent=2, ensure_ascii=False, 
                         default=self.serialize_datetime)
            self.stdout.write(self.style.SUCCESS(
                f'✓ Exportados {len(repartidores)} repartidores a repartidores_export.json'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error exportando repartidores: {e}'))
        
        # Exportar notificaciones
        try:
            notificaciones = list(NotificacionProblema.objects.all().values())
            with open('notificaciones_export.json', 'w', encoding='utf-8') as f:
                json.dump(notificaciones, f, indent=2, ensure_ascii=False,
                         default=self.serialize_datetime)
            self.stdout.write(self.style.SUCCESS(
                f'✓ Exportadas {len(notificaciones)} notificaciones a notificaciones_export.json'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error exportando notificaciones: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Exportación completada'))

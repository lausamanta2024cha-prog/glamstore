#!/usr/bin/env python
"""
Script para exportar datos de repartidores y notificaciones a JSON
"""
import os
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.repartidores import Repartidor
from core.models.notificaciones import NotificacionProblema

def serialize_datetime(obj):
    """Serializar datetime a string ISO"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def export_repartidores():
    """Exportar todos los repartidores"""
    repartidores = Repartidor.objects.all().values()
    data = list(repartidores)
    
    with open('repartidores_export.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=serialize_datetime)
    
    print(f"✓ Exportados {len(data)} repartidores a repartidores_export.json")

def export_notificaciones():
    """Exportar todas las notificaciones de problemas"""
    notificaciones = NotificacionProblema.objects.all().values()
    data = list(notificaciones)
    
    with open('notificaciones_export.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=serialize_datetime)
    
    print(f"✓ Exportadas {len(data)} notificaciones a notificaciones_export.json")

if __name__ == '__main__':
    print("Exportando datos...")
    export_repartidores()
    export_notificaciones()
    print("\n✓ Exportación completada")

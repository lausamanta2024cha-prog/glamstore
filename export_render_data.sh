#!/bin/bash
# Script para exportar datos de Render a archivos JSON

echo "Exportando datos de Render..."

# Exportar repartidores
python manage.py shell << EOF
import json
from datetime import datetime
from core.models.repartidores import Repartidor
from core.models.notificaciones import NotificacionProblema

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

# Exportar repartidores
repartidores = list(Repartidor.objects.all().values())
with open('repartidores_export.json', 'w', encoding='utf-8') as f:
    json.dump(repartidores, f, indent=2, ensure_ascii=False, default=serialize_datetime)
print(f"✓ Exportados {len(repartidores)} repartidores")

# Exportar notificaciones
notificaciones = list(NotificacionProblema.objects.all().values())
with open('notificaciones_export.json', 'w', encoding='utf-8') as f:
    json.dump(notificaciones, f, indent=2, ensure_ascii=False, default=serialize_datetime)
print(f"✓ Exportadas {len(notificaciones)} notificaciones")
EOF

echo "✓ Exportación completada"

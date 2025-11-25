import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.pedidos import Pedido
from core.models.repartidores import Repartidor

# Ver pedidos sin repartidor
pedidos_sin_repartidor = Pedido.objects.filter(idRepartidor__isnull=True)
print(f"Total pedidos sin repartidor: {pedidos_sin_repartidor.count()}")

# Ver estados de esos pedidos
estados = pedidos_sin_repartidor.values_list('estado_pedido', flat=True).distinct()
print(f"Estados de pedidos sin repartidor: {list(estados)}")

# Contar por estado
for estado in estados:
    count = pedidos_sin_repartidor.filter(estado_pedido=estado).count()
    print(f"  - {estado}: {count}")

# Ver repartidores disponibles
repartidores = Repartidor.objects.filter(estado_turno='Disponible')
print(f"\nRepartidores disponibles: {repartidores.count()}")
for r in repartidores:
    print(f"  - {r.nombreRepartidor} (ID: {r.idRepartidor})")

# Ver todos los repartidores
todos_repartidores = Repartidor.objects.all()
print(f"\nTodos los repartidores: {todos_repartidores.count()}")
for r in todos_repartidores:
    print(f"  - {r.nombreRepartidor}: {r.estado_turno}")

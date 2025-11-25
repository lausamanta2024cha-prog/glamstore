import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.pedidos import Pedido
from core.Gestion_admin.services_repartidores import enviar_factura_cliente

# Buscar un pedido con repartidor asignado
pedido = Pedido.objects.filter(idRepartidor__isnull=False).select_related('idCliente', 'idRepartidor').first()

if pedido:
    print(f"Pedido: #{pedido.idPedido}")
    print(f"Cliente: {pedido.idCliente.nombre}")
    print(f"Email cliente: {pedido.idCliente.email}")
    print(f"Repartidor: {pedido.idRepartidor.nombreRepartidor}")
    print(f"Estado pago: {pedido.estado_pago}")
    print(f"Total: ${pedido.total}")
    print()
    print("Enviando factura...")
    resultado = enviar_factura_cliente(pedido)
    print(f"Resultado: {'Enviado' if resultado else 'Error'}")
else:
    print("No hay pedidos con repartidor asignado")

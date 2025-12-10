from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Pedido, Cliente


class Command(BaseCommand):
    help = 'Actualiza las fechas de vencimiento estimadas de los pedidos basadas en su ubicación'

    def handle(self, *args, **options):
        # Obtener todos los pedidos que no tienen fecha de vencimiento
        pedidos_sin_vencimiento = Pedido.objects.filter(fecha_vencimiento__isnull=True)
        
        actualizado = 0
        for pedido in pedidos_sin_vencimiento:
            try:
                cliente = pedido.idCliente
                if not cliente:
                    self.stdout.write(f"Pedido {pedido.idPedido}: Sin cliente asociado")
                    continue
                
                # Determinar días de entrega basado en ubicación
                direccion_lower = (cliente.direccion or "").lower()
                if 'soacha' in direccion_lower:
                    dias_entrega = 3
                elif 'bogota' in direccion_lower or 'bogotá' in direccion_lower:
                    dias_entrega = 2
                else:
                    dias_entrega = 3
                
                # Calcular fecha de vencimiento
                fecha_vencimiento = (pedido.fechaCreacion + timedelta(days=dias_entrega)).date()
                
                # Actualizar pedido
                pedido.fecha_vencimiento = fecha_vencimiento
                pedido.save()
                
                actualizado += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Pedido {pedido.idPedido}: Fecha vencimiento establecida a {fecha_vencimiento} ({dias_entrega} días)"
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error al procesar pedido {pedido.idPedido}: {str(e)}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"\nTotal de pedidos actualizados: {actualizado}")
        )

from django.db import models


class Pedido(models.Model):
    idPedido = models.AutoField(primary_key=True)
    fechaCreacion = models.DateTimeField(db_column='fechaCreacion') # Asumiendo que la columna se llama así
    estado = models.CharField(max_length=20)  # Estado del pedido: En Camino, Entregado, etc.
    total = models.DecimalField(max_digits=12, decimal_places=2)
    idCliente = models.ForeignKey('core.Cliente', on_delete=models.CASCADE, db_column='idCliente')
    idRepartidor = models.ForeignKey(
        'core.Repartidor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='idRepartidor'
    )
    
    # Método para obtener el estado de pago
    def get_estado_pago(self):
        """
        Determina el estado de pago basándose en el estado actual y la lógica del negocio.
        """
        if self.estado == 'Pago Parcial':
            return 'Pago Parcial'
        elif self.estado in ['Entregado', 'Completado']:
            # Cuando se entrega, el pago siempre se completa (se cobró el envío)
            return 'Pago Completo'
        else:
            # Para otros estados, asumir pago completo
            return 'Pago Completo'
    
    # Método para obtener el estado limpio del pedido
    def get_estado_pedido(self):
        """
        Obtiene el estado del pedido para mostrar al cliente.
        """
        if self.estado == 'Pago Parcial' and self.idRepartidor:
            # Si tiene repartidor asignado, está en camino
            return 'En Camino'
        elif self.estado == 'Pago Parcial':
            # Si no tiene repartidor, está confirmado
            return 'Confirmado'
        elif self.estado == 'Pago Completo':
            # Si pagó completo pero no tiene repartidor, está confirmado
            if self.idRepartidor:
                return 'En Camino'
            else:
                return 'Confirmado'
        else:
            # Para otros estados, devolver tal como está
            return self.estado


    class Meta:
        db_table = 'pedidos'
        managed = False
        app_label = 'core'

    def __str__(self):
        return f"Pedido #{self.idPedido} - {self.estado}"


class DetallePedido(models.Model):
    idDetalle = models.AutoField(primary_key=True)
    idPedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column='idPedido'
    )
    idProducto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        db_column='idProducto'
    )
    cantidad = models.PositiveIntegerField(default=1, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'detallepedido'
        managed = False
        app_label = 'core'

    def __str__(self):
        return f"Detalle #{self.idDetalle} - Producto {self.idProducto_id}"


class PedidoProducto(models.Model):
    idPedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column='idPedido'
    )
    idProducto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        db_column='idProducto'
    )
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'pedidoproducto'
        managed = False
        app_label = 'core'
        unique_together = ('idPedido', 'idProducto')

    def __str__(self):
        return f"Pedido {self.idPedido_id} - Producto {self.idProducto_id}"
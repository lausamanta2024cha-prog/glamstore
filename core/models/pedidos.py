from django.db import models


class Pedido(models.Model):
    ESTADO_PAGO_CHOICES = [
        ('Pago Completo', 'Pago Completo'),
        ('Pago Parcial', 'Pago Parcial'),
    ]
    
    ESTADO_PEDIDO_CHOICES = [
        ('Pedido Recibido', 'Pedido Recibido'),
        ('Pago Confirmado', 'Pago Confirmado'),
        ('En Preparación', 'En Preparación'),
        ('En Camino', 'En Camino'),
        ('Entregado', 'Entregado'),
        ('Completado', 'Completado'),
        ('Problema en Entrega', 'Problema en Entrega'),
    ]
    
    idPedido = models.AutoField(primary_key=True)
    fechaCreacion = models.DateTimeField(db_column='fechaCreacion', null=True, blank=True)
    estado = models.CharField(max_length=20, default='Pedido Recibido')  # Mantener para compatibilidad
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='Pago Completo')
    estado_pedido = models.CharField(max_length=20, choices=ESTADO_PEDIDO_CHOICES, default='Pedido Recibido')
    total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    idCliente = models.ForeignKey('core.Cliente', on_delete=models.CASCADE, db_column='idCliente', null=True, blank=True)
    idRepartidor = models.ForeignKey(
        'core.Repartidor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='idRepartidor'
    )
    fecha_vencimiento = models.DateField(null=True, blank=True, db_column='fechaVencimiento')
    facturas_enviadas = models.PositiveIntegerField(default=0, db_column='facturasEnviadas')
    
    # Método para obtener el estado de pago (compatibilidad)
    def get_estado_pago(self):
        """
        Retorna el estado de pago del pedido.
        """
        return self.estado_pago
    
    # Método para obtener el estado del pedido (compatibilidad)
    def get_estado_pedido(self):
        """
        Retorna el estado del pedido.
        """
        return self.estado_pedido


    class Meta:
        db_table = 'pedidos'
        managed = True
        app_label = 'core'

    def __str__(self):
        return f"Pedido #{self.idPedido} - {self.estado}"


class DetallePedido(models.Model):
    idDetalle = models.AutoField(primary_key=True)
    idPedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column='idPedido',
        null=True,
        blank=True
    )
    idProducto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        db_column='idProducto',
        null=True,
        blank=True
    )
    cantidad = models.PositiveIntegerField(default=1, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    margen_ganancia = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=10,
        help_text="Margen de ganancia que se cobró en este pedido"
    )

    class Meta:
        db_table = 'detallepedido'
        managed = True
        app_label = 'core'

    def __str__(self):
        return f"Detalle #{self.idDetalle} - Producto {self.idProducto_id}"


class PedidoProducto(models.Model):
    idPedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column='idPedido',
        null=True,
        blank=True
    )
    idProducto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        db_column='idProducto',
        null=True,
        blank=True
    )
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'pedidoproducto'
        managed = True
        app_label = 'core'
        unique_together = ('idPedido', 'idProducto')

    def __str__(self):
        return f"Pedido {self.idPedido_id} - Producto {self.idProducto_id}"
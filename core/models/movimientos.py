from django.db import models
from .productos import Producto
from .pedidos import Pedido
from decimal import Decimal

class MovimientoProducto(models.Model):
    idMovimiento = models.AutoField(primary_key=True, db_column='idmovimiento')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos', db_column='producto_id')
    fecha = models.DateTimeField(auto_now_add=True, db_column='fecha')
    tipo_movimiento = models.CharField(max_length=50, db_column='tipo_movimiento', choices=[
        ('ENTRADA_INICIAL', 'Entrada Inicial'),
        ('AJUSTE_MANUAL_ENTRADA', 'Ajuste Manual (Entrada)'),
        ('AJUSTE_MANUAL_SALIDA', 'Ajuste Manual (Salida)'),
        ('SALIDA_VENTA', 'Salida por Venta'),
        ('EN_PREPARACION_SALIDA', 'En Preparación (Apartado)'),
        ('PERDIDA_VENCIMIENTO', 'Pérdida por Vencimiento'),
    ])
    cantidad = models.IntegerField(db_column='cantidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column='precio_unitario')
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column='costo_unitario', help_text="Costo por unidad para movimientos de entrada.")
    stock_anterior = models.IntegerField(db_column='stock_anterior')
    stock_nuevo = models.IntegerField(db_column='stock_nuevo')
    id_pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True, db_column='idpedido')
    descripcion = models.CharField(max_length=255, blank=True, null=True, db_column='descripcion')
    
    # Campos adicionales para reabastecimiento
    lote = models.CharField(max_length=100, blank=True, null=True, db_column='lote', help_text="Código del lote del producto")
    fecha_vencimiento = models.DateField(blank=True, null=True, db_column='fecha_vencimiento', help_text="Fecha de vencimiento del producto")
    total_con_iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='total_con_iva', help_text="Total incluyendo IVA")
    iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='iva', help_text="Valor del IVA (19%)")
    
    # Campo para trazabilidad de lotes (para salidas)
    lote_origen = models.ForeignKey('LoteProducto', on_delete=models.SET_NULL, null=True, blank=True, db_column='lote_origen_id',
                                   help_text="Lote del cual salió el producto (para movimientos de salida)")

    class Meta:
        db_table = 'movimientos_producto'
        ordering = ['-fecha']
        app_label = 'core'

    def __str__(self):
        return f"Movimiento de {self.producto.nombreProducto} el {self.fecha}"

    @property
    def valor_movimiento(self):
        if 'ENTRADA' in self.tipo_movimiento and self.costo_unitario > 0:
            return self.costo_unitario * self.cantidad
        return 0

    @property
    def precio_venta_recomendado(self):
        """Calcula el precio de venta recomendado (precio unitario + 25%)"""
        if self.precio_unitario and self.precio_unitario > 0:
            return self.precio_unitario * Decimal('1.25')
        return 0
    
    @property
    def ganancia_por_unidad(self):
        """Calcula la ganancia por unidad (precio venta - precio unitario)"""
        if self.precio_unitario and self.precio_unitario > 0:
            return self.precio_venta_recomendado - self.precio_unitario
        return 0
    
    @property
    def ganancia_estimada(self):
        """Calcula la ganancia total (ganancia por unidad × cantidad)"""
        return self.ganancia_por_unidad * Decimal(self.cantidad)
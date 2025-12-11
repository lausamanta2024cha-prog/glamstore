from django.db import models
from .productos import Producto
from decimal import Decimal

class LoteProducto(models.Model):
    """
    Modelo para manejar lotes de productos con trazabilidad FIFO
    """
    idLote = models.AutoField(primary_key=True, db_column='idlote')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes', db_column='producto_id')
    codigo_lote = models.CharField(max_length=100, db_column='codigo_lote', help_text="Código único del lote")
    fecha_entrada = models.DateTimeField(auto_now_add=True, db_column='fecha_entrada')
    fecha_vencimiento = models.DateField(null=True, blank=True, db_column='fecha_vencimiento')
    cantidad_inicial = models.IntegerField(db_column='cantidad_inicial', help_text="Cantidad inicial del lote")
    cantidad_disponible = models.IntegerField(db_column='cantidad_disponible', help_text="Cantidad disponible actual")
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column='costo_unitario')
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column='precio_venta')
    
    # Campos de IVA
    total_con_iva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='total_con_iva')
    iva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='iva')
    
    # Información del proveedor
    proveedor = models.CharField(max_length=200, null=True, blank=True, db_column='proveedor')
    
    class Meta:
        db_table = 'lotes_producto'
        ordering = ['fecha_entrada']  # FIFO: primero en entrar, primero en salir
        app_label = 'core'
        unique_together = ['producto', 'codigo_lote']
    
    def __str__(self):
        return f"Lote {self.codigo_lote} - {self.producto.nombreProducto}"
    
    @property
    def esta_agotado(self):
        return self.cantidad_disponible <= 0
    
    @property
    def porcentaje_usado(self):
        if self.cantidad_inicial > 0:
            return ((self.cantidad_inicial - self.cantidad_disponible) / self.cantidad_inicial) * 100
        return 0


class MovimientoLote(models.Model):
    """
    Modelo para rastrear movimientos específicos de lotes
    """
    idMovimientoLote = models.AutoField(primary_key=True, db_column='idmovimientolote')
    lote = models.ForeignKey(LoteProducto, on_delete=models.CASCADE, related_name='movimientos', db_column='lote_id')
    movimiento_producto = models.ForeignKey('MovimientoProducto', on_delete=models.CASCADE, related_name='movimientos_lote', db_column='movimiento_producto_id')
    cantidad = models.IntegerField(db_column='cantidad', help_text="Cantidad tomada de este lote")
    fecha = models.DateTimeField(auto_now_add=True, db_column='fecha')
    
    class Meta:
        db_table = 'movimientos_lote'
        ordering = ['-fecha']
        app_label = 'core'
    
    def __str__(self):
        return f"Movimiento de {self.cantidad} unidades del lote {self.lote.codigo_lote}"
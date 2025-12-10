from django.db import models


class Producto(models.Model):
    idProducto = models.BigAutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)
    lote = models.CharField(max_length=100, blank=True, null=True, help_text="Código del lote actual")
    cantidadDisponible = models.IntegerField(default=0, db_column='cantidadDisponible')
    fechaIngreso = models.DateTimeField(blank=True, null=True, db_column='fechaIngreso')
    fechaVencimiento = models.DateField(blank=True, null=True, db_column='fechaVencimiento')

    idCategoria = models.ForeignKey(
        'Categoria',
        on_delete=models.SET_NULL,
        null=True,
        db_column='idCategoria'
    )

    idSubcategoria = models.ForeignKey(
        'Subcategoria',
        on_delete=models.SET_NULL,
        null=True,
        db_column='idSubcategoria'
    )

    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Precio de venta calculado automáticamente")

    class Meta:
        db_table = 'productos'
        managed = False # Cambiado a False para coincidir con otros modelos
        app_label = 'core'

    def __str__(self):
        return self.nombreProducto
    
    def calcular_precio_venta(self):
        """Calcula el precio de venta: Costo × 1.19 (IVA) × (1 + margen_ganancia_global/100)
        Redondea al múltiplo de 50 más cercano para precios limpios"""
        from decimal import Decimal
        from core.models.configuracion import ConfiguracionGlobal
        
        if self.precio:
            # Convertir precio a Decimal si es string
            precio_decimal = Decimal(str(self.precio)) if not isinstance(self.precio, Decimal) else self.precio
            # Obtener el margen global
            margen = Decimal(str(ConfiguracionGlobal.get_margen_ganancia()))
            # Precio de Venta = Costo × 1.19 (IVA) × (1 + margen/100)
            factor_margen = Decimal('1') + (margen / Decimal('100'))
            precio_calculado = float(precio_decimal * Decimal('1.19') * factor_margen)
            # Redondear al múltiplo de 50 más cercano
            precio_redondeado = round(precio_calculado / 50) * 50
            return int(precio_redondeado)
        return 0
    
    def save(self, *args, **kwargs):
        """Sobrescribe el método save para calcular automáticamente el precio_venta"""
        # Calcular precio_venta antes de guardar
        self.precio_venta = self.calcular_precio_venta()
        super().save(*args, **kwargs)

from django.db import models


class Producto(models.Model):
    idProducto = models.BigAutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)

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

    class Meta:
        db_table = 'productos'
        managed = False # Cambiado a False para coincidir con otros modelos
        app_label = 'core'

    def __str__(self):
        return self.nombreProducto
    
    @property
    def precio_venta(self):
        """Calcula el precio de venta (precio unitario + 30%)"""
        from decimal import Decimal
        if self.precio:
            return self.precio * Decimal('1.30')
        return 0

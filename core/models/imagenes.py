from django.db import models

class ImagenProducto(models.Model):
    """Modelo para almacenar imágenes de productos en la base de datos"""
    idProducto = models.BigIntegerField(db_column='id_producto')
    nombreArchivo = models.CharField(max_length=255, db_column='nombre_archivo')
    ruta = models.CharField(max_length=255, db_column='ruta')  # ej: 'productos/rubor.jpg'
    contenido = models.BinaryField(db_column='contenido')  # Imagen en binario
    fechaSubida = models.DateTimeField(auto_now_add=True, db_column='fecha_subida')
    
    class Meta:
        db_table = 'imagenes_productos'
        managed = False
        app_label = 'core'
    
    def __str__(self):
        return f"Imagen {self.nombreArchivo} - Producto {self.idProducto}"


class ImagenCategoria(models.Model):
    """Modelo para almacenar imágenes de categorías en la base de datos"""
    idCategoria = models.IntegerField(db_column='id_categoria')
    nombreArchivo = models.CharField(max_length=255, db_column='nombre_archivo')
    ruta = models.CharField(max_length=255, db_column='ruta')  # ej: 'categorias/rostro.avif'
    contenido = models.BinaryField(db_column='contenido')  # Imagen en binario
    fechaSubida = models.DateTimeField(auto_now_add=True, db_column='fecha_subida')
    
    class Meta:
        db_table = 'imagenes_categorias'
        managed = False
        app_label = 'core'
    
    def __str__(self):
        return f"Imagen {self.nombreArchivo} - Categoría {self.idCategoria}"

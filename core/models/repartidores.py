from django.db import models
from django.db import connection

class Repartidor(models.Model):
    idRepartidor = models.AutoField(primary_key=True)
    nombreRepartidor = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    estado_turno = models.CharField(max_length=20, null=True, default='Disponible')

    class Meta:
        db_table = 'repartidores'   
        managed = False             
        app_label = 'core'
    
    def __str__(self):
        return self.nombreRepartidor or f"Repartidor {self.idRepartidor}"
    
    @classmethod
    def ensure_email_column_exists(cls):
        """Asegura que la columna email existe en la tabla"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'repartidores' 
                    AND COLUMN_NAME = 'email'
                """)
                if not cursor.fetchone():
                    cursor.execute("""
                        ALTER TABLE repartidores 
                        ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL
                    """)
        except Exception:
            pass  # Ignorar errores si la columna ya existe
    
    @classmethod
    def ensure_telefono_column_size(cls):
        """Asegura que la columna telefono tiene el tamaño correcto"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COLUMN_TYPE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'repartidores' 
                    AND COLUMN_NAME = 'telefono'
                """)
                result = cursor.fetchone()
                if result and 'varchar(11)' in result[0].lower():
                    # Aumentar el tamaño del campo
                    cursor.execute("""
                        ALTER TABLE repartidores 
                        MODIFY COLUMN telefono VARCHAR(20) NULL
                    """)
        except Exception:
            pass  # Ignorar errores     

        
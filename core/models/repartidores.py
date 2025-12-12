from django.db import models
from django.db import connection

class Repartidor(models.Model):
    idRepartidor = models.AutoField(primary_key=True, db_column='idrepartidor')
    nombreRepartidor = models.CharField(max_length=50, null=True, db_column='nombre')
    telefono = models.CharField(max_length=20, null=True, db_column='telefono')
    email = models.EmailField(max_length=100, null=True, blank=True, db_column='email')

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
                # Intentar con PostgreSQL primero
                try:
                    cursor.execute("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'repartidores' 
                        AND column_name = 'email'
                    """)
                    if not cursor.fetchone():
                        cursor.execute("""
                            ALTER TABLE repartidores 
                            ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL
                        """)
                except:
                    # Si falla, intentar con MySQL
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
            pass 
    
    @classmethod
    def ensure_telefono_column_size(cls):
        """Asegura que la columna telefono tiene el tamaño correcto"""
        try:
            with connection.cursor() as cursor:
                # Intentar con PostgreSQL primero
                try:
                    cursor.execute("""
                        SELECT data_type 
                        FROM information_schema.columns 
                        WHERE table_name = 'repartidores' 
                        AND column_name = 'telefono'
                    """)
                    result = cursor.fetchone()
                    if result:
                        cursor.execute("""
                            ALTER TABLE repartidores 
                            ALTER COLUMN telefono TYPE VARCHAR(20)
                        """)
                except:
                    # Si falla, intentar con MySQL
                    cursor.execute("""
                        SELECT COLUMN_TYPE 
                        FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_NAME = 'repartidores' 
                        AND COLUMN_NAME = 'telefono'
                    """)
                    result = cursor.fetchone()
                    if result and 'varchar(11)' in result[0].lower():
                        cursor.execute("""
                            ALTER TABLE repartidores 
                            MODIFY COLUMN telefono VARCHAR(20) NULL
                        """)
        except Exception:
            pass     

        
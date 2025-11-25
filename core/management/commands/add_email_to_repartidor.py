from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Agrega la columna email a la tabla repartidores'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                # Verificar si la columna ya existe
                cursor.execute("""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'repartidores' 
                    AND COLUMN_NAME = 'email'
                """)
                
                if cursor.fetchone():
                    self.stdout.write(self.style.SUCCESS("La columna 'email' ya existe en la tabla 'repartidores'"))
                else:
                    # Agregar la columna
                    cursor.execute("""
                        ALTER TABLE repartidores 
                        ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL
                    """)
                    self.stdout.write(self.style.SUCCESS("Columna 'email' agregada exitosamente a la tabla 'repartidores'"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

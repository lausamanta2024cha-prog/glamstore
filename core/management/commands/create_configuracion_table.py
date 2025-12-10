from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Crea la tabla configuracion_global'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS configuracion_global (
                        id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        margen_ganancia DECIMAL(5, 2) DEFAULT 10,
                        fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                ''')
                
                # Insertar un registro por defecto si no existe
                cursor.execute('SELECT COUNT(*) FROM configuracion_global')
                count = cursor.fetchone()[0]
                
                if count == 0:
                    cursor.execute('''
                        INSERT INTO configuracion_global (id, margen_ganancia) 
                        VALUES (1, 10)
                    ''')
                
                self.stdout.write(self.style.SUCCESS('Tabla configuracion_global creada exitosamente'))
            except Exception as e:
                if 'already exists' in str(e):
                    self.stdout.write(self.style.WARNING('La tabla configuracion_global ya existe'))
                else:
                    self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

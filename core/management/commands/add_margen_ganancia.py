from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Agrega la columna margen_ganancia a la tabla productos'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                cursor.execute('''
                    ALTER TABLE productos 
                    ADD COLUMN margen_ganancia DECIMAL(5, 2) DEFAULT 10
                ''')
                self.stdout.write(self.style.SUCCESS('Columna margen_ganancia agregada exitosamente'))
            except Exception as e:
                if 'Duplicate column' in str(e):
                    self.stdout.write(self.style.WARNING('La columna margen_ganancia ya existe'))
                else:
                    self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

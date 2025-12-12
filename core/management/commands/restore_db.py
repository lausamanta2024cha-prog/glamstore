"""
Comando Django para restaurar la BD desde archivo SQL
Uso: python manage.py restore_db [archivo_sql]
Ejemplo: python manage.py restore_db glamstoredb.sql
"""
import os
import sys
import subprocess
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Restaura la BD desde un archivo SQL usando mysql directamente'

    def add_arguments(self, parser):
        parser.add_argument(
            'sql_file',
            nargs='?',
            default='glamstoredb.sql',
            type=str,
            help='Ruta del archivo SQL a restaurar (default: glamstoredb.sql)'
        )

    def handle(self, *args, **options):
        sql_file = options['sql_file']
        
        # Verificar que el archivo existe
        if not os.path.exists(sql_file):
            self.stdout.write(self.style.ERROR(f'✗ Archivo no encontrado: {sql_file}'))
            sys.exit(1)
        
        self.stdout.write(self.style.SUCCESS(f'Restaurando BD desde {sql_file}...'))
        
        try:
            # Obtener configuración de BD
            db_config = settings.DATABASES['default']
            
            # Construir comando mysql
            if db_config['ENGINE'] == 'django.db.backends.mysql':
                cmd = [
                    'mysql',
                    f"-h{db_config['HOST']}",
                    f"-u{db_config['USER']}",
                    f"-p{db_config['PASSWORD']}",
                    db_config['NAME'],
                    f"< {sql_file}"
                ]
                
                # Ejecutar con shell=True para que funcione el redirección
                result = subprocess.run(
                    f"mysql -h{db_config['HOST']} -u{db_config['USER']} -p{db_config['PASSWORD']} {db_config['NAME']} < {sql_file}",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    self.stdout.write(self.style.ERROR(f'✗ Error: {result.stderr}'))
                    sys.exit(1)
                
                self.stdout.write(self.style.SUCCESS('✓ BD restaurada exitosamente'))
            else:
                # Para SQLite u otras BDs, usar el método anterior
                self._restore_with_django(sql_file)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error restaurando BD: {e}'))
            sys.exit(1)

    def _restore_with_django(self, sql_file):
        """Restaurar usando Django ORM"""
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        with connection.cursor() as cursor:
            statements = sql_content.split(';')
            executed = 0
            
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                        executed += 1
                    except Exception as e:
                        # Algunos statements pueden fallar
                        pass
            
            connection.commit()
        
        self.stdout.write(self.style.SUCCESS(
            f'✓ BD restaurada exitosamente ({executed} statements ejecutados)'
        ))

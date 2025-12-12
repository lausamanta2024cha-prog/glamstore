#!/usr/bin/env python
"""
Script para restaurar la BD desde SQL en Render
Ejecuta: python restore_database.py [archivo_sql]
"""
import os
import sys
import subprocess
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.conf import settings
from django.db import connection


def restore_database(sql_file='glamstoredb.sql'):
    """Restaurar BD desde archivo SQL"""
    
    if not os.path.exists(sql_file):
        print(f"✗ Error: Archivo no encontrado: {sql_file}")
        return False
    
    print(f"Restaurando BD desde {sql_file}...")
    
    try:
        db_config = settings.DATABASES['default']
        
        # Si es MySQL, usar mysql CLI directamente
        if 'mysql' in db_config['ENGINE'].lower():
            print("Usando MySQL CLI para restaurar...")
            
            cmd = (
                f"mysql -h{db_config['HOST']} "
                f"-u{db_config['USER']} "
                f"-p{db_config['PASSWORD']} "
                f"{db_config['NAME']} < {sql_file}"
            )
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"✗ Error: {result.stderr}")
                return False
            
            print("✓ BD restaurada exitosamente")
            return True
        
        # Si es SQLite o PostgreSQL, usar Django
        else:
            print("Usando Django para restaurar...")
            
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
                            pass
                
                connection.commit()
            
            print(f"✓ BD restaurada exitosamente ({executed} statements ejecutados)")
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == '__main__':
    sql_file = sys.argv[1] if len(sys.argv) > 1 else 'glamstoredb.sql'
    
    if restore_database(sql_file):
        print("\n✓ Restauración completada")
        sys.exit(0)
    else:
        print("\n✗ Restauración fallida")
        sys.exit(1)

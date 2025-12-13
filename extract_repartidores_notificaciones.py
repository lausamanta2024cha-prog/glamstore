#!/usr/bin/env python
"""
Extraer e insertar repartidores y notificaciones desde el SQL
"""
import re
import psycopg2
from django.conf import settings
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

def extract_inserts(sql_file, table_names):
    """Extraer INSERT statements para tablas específicas"""
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    inserts = []
    
    for table in table_names:
        # Buscar INSERT INTO "tabla"
        pattern = rf'INSERT INTO "{table}"[^;]*;'
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        inserts.extend(matches)
    
    return inserts

def insert_data(inserts):
    """Insertar datos en la BD"""
    db_config = settings.DATABASES['default']
    
    conn = psycopg2.connect(
        host=db_config['HOST'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        database=db_config['NAME'],
        port=db_config['PORT']
    )
    
    cursor = conn.cursor()
    
    print(f"Insertando {len(inserts)} statements...")
    
    for i, insert in enumerate(inserts, 1):
        try:
            cursor.execute(insert)
            conn.commit()
            print(f"✓ {i}/{len(inserts)}")
        except Exception as e:
            conn.rollback()
            print(f"✗ {i}: {str(e)[:80]}")
    
    cursor.close()
    conn.close()
    
    print("✓ Completado")

if __name__ == '__main__':
    # Extraer repartidores y notificaciones
    tables = ['repartidores', 'notificaciones_problema']
    
    print("Extrayendo INSERT statements...")
    inserts = extract_inserts('glamstoredb_postgres.sql', tables)
    
    print(f"Encontrados {len(inserts)} statements")
    
    if inserts:
        insert_data(inserts)
    else:
        print("No se encontraron statements")

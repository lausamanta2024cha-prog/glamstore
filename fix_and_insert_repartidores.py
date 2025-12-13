#!/usr/bin/env python
"""
Corregir y insertar repartidores desde el SQL
"""
import re
import psycopg2
from django.conf import settings
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

def fix_repartidores_insert(sql_file):
    """Extraer y corregir INSERT de repartidores"""
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar INSERT INTO "repartidores"
    pattern = r'INSERT INTO "repartidores"\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\)'
    
    matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
    
    inserts = []
    for match in matches:
        columns_str = match.group(1)
        values_str = match.group(2)
        
        # Reemplazar nombreRepartidor por nombre
        columns_str = columns_str.replace('"nombreRepartidor"', '"nombre"')
        columns_str = columns_str.replace('"estado_turno"', '')  # Remover esta columna
        
        # Limpiar columnas vacías
        columns = [c.strip() for c in columns_str.split(',') if c.strip()]
        
        # Reconstruir el INSERT
        insert = f'INSERT INTO "repartidores" ({", ".join(columns)}) VALUES ({values_str});'
        inserts.append(insert)
    
    return inserts

def insert_repartidores(inserts):
    """Insertar repartidores en la BD"""
    db_config = settings.DATABASES['default']
    
    conn = psycopg2.connect(
        host=db_config['HOST'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        database=db_config['NAME'],
        port=db_config['PORT']
    )
    
    cursor = conn.cursor()
    
    print(f"Insertando {len(inserts)} repartidores...")
    
    for i, insert in enumerate(inserts, 1):
        try:
            cursor.execute(insert)
            conn.commit()
            print(f"✓ Repartidor {i}/{len(inserts)}")
        except Exception as e:
            conn.rollback()
            print(f"✗ Repartidor {i}: {str(e)[:100]}")
    
    cursor.close()
    conn.close()
    
    print("✓ Completado")

if __name__ == '__main__':
    print("Extrayendo y corrigiendo INSERT de repartidores...")
    inserts = fix_repartidores_insert('glamstoredb_postgres.sql')
    
    print(f"Encontrados {len(inserts)} repartidores")
    
    if inserts:
        insert_repartidores(inserts)
    else:
        print("No se encontraron repartidores")

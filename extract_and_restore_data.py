#!/usr/bin/env python
"""
Script para extraer datos del SQL MySQL y restaurarlos en PostgreSQL
Ejecuta: python extract_and_restore_data.py
"""
import os
import sys
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.conf import settings
import psycopg2


def extract_insert_statements(sql_file):
    """Extraer solo los INSERT statements del SQL"""
    print(f"Leyendo {sql_file}...")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Buscar todos los INSERT statements
    insert_pattern = r'INSERT INTO\s+`?(\w+)`?\s*\([^)]+\)\s+VALUES\s*\([^)]+(?:\),\s*\([^)]+\))*\);'
    inserts = re.findall(insert_pattern, sql_content, re.IGNORECASE | re.DOTALL)
    
    print(f"✓ Encontrados {len(inserts)} INSERT statements\n")
    
    # Extraer los INSERT statements completos
    insert_statements = []
    for match in re.finditer(insert_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        insert_statements.append(match.group(0))
    
    return insert_statements


def convert_insert_to_postgres(insert_statement):
    """Convertir un INSERT statement de MySQL a PostgreSQL"""
    # Reemplazar backticks por comillas dobles
    statement = insert_statement.replace('`', '"')
    
    # Remover comentarios MySQL especiales
    statement = re.sub(r'/\*!\d+[^*]*\*/', '', statement)
    
    return statement


def restore_data(insert_statements):
    """Restaurar los datos en PostgreSQL"""
    db_config = settings.DATABASES['default']
    
    print("Conectando a PostgreSQL...")
    print(f"Host: {db_config['HOST']}")
    print(f"BD: {db_config['NAME']}\n")
    
    try:
        conn = psycopg2.connect(
            host=db_config['HOST'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            database=db_config['NAME'],
            port=db_config['PORT']
        )
        
        cursor = conn.cursor()
        executed = 0
        failed = 0
        
        print(f"Ejecutando {len(insert_statements)} INSERT statements...\n")
        
        for i, statement in enumerate(insert_statements):
            try:
                # Convertir a PostgreSQL
                pg_statement = convert_insert_to_postgres(statement)
                
                # Ejecutar
                cursor.execute(pg_statement)
                executed += 1
                
                # Mostrar progreso
                if (i + 1) % 10 == 0:
                    print(f"  ✓ {i + 1}/{len(insert_statements)} statements ejecutados")
                    
            except Exception as e:
                failed += 1
                if failed <= 3:
                    print(f"  ⚠ Error en statement {i + 1}: {str(e)[:80]}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n✓ Restauración completada")
        print(f"  - Ejecutados: {executed}")
        print(f"  - Fallidos: {failed}")
        
        # Verificar datos
        print(f"\nVerificando datos...")
        conn = psycopg2.connect(
            host=db_config['HOST'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            database=db_config['NAME'],
            port=db_config['PORT']
        )
        
        cursor = conn.cursor()
        
        # Contar datos importantes
        tables_to_check = [
            ('repartidores', 'Repartidores'),
            ('notificaciones_problema', 'Notificaciones'),
            ('roles', 'Roles'),
            ('usuarios', 'Usuarios'),
            ('pedidos', 'Pedidos'),
        ]
        
        for table, label in tables_to_check:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM "{table}";')
                count = cursor.fetchone()[0]
                print(f"  - {label}: {count}")
            except:
                print(f"  - {label}: tabla no encontrada")
        
        cursor.close()
        conn.close()
        
        print(f"\n✓ Proceso completado exitosamente")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("EXTRAER Y RESTAURAR DATOS DE SQL")
    print("=" * 60 + "\n")
    
    # Aceptar nombre de archivo como parámetro
    sql_file = sys.argv[1] if len(sys.argv) > 1 else 'glamstoredb.sql'
    
    if not os.path.exists(sql_file):
        print(f"✗ Archivo no encontrado: {sql_file}")
        sys.exit(1)
    
    try:
        # Extraer INSERT statements
        insert_statements = extract_insert_statements(sql_file)
        
        if not insert_statements:
            print("✗ No se encontraron INSERT statements")
            sys.exit(1)
        
        # Restaurar datos
        restore_data(insert_statements)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

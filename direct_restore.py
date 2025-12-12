#!/usr/bin/env python
"""
Script directo para restaurar BD desde SQL en Render
Ejecuta: python direct_restore.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.conf import settings
import psycopg2


def parse_sql_statements(sql_content):
    """Parsear statements SQL"""
    statements = []
    current_statement = []
    in_string = False
    string_char = None
    
    for i, char in enumerate(sql_content):
        # Detectar inicio/fin de strings
        if char in ('"', "'") and (i == 0 or sql_content[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
        
        # Si encontramos ; fuera de un string, es fin de statement
        if char == ';' and not in_string:
            current_statement.append(char)
            statement = ''.join(current_statement).strip()
            
            # Filtrar comentarios y líneas vacías
            if statement and not statement.startswith('--'):
                statements.append(statement)
            
            current_statement = []
        else:
            current_statement.append(char)
    
    # Agregar último statement si existe
    if current_statement:
        statement = ''.join(current_statement).strip()
        if statement and not statement.startswith('--'):
            statements.append(statement)
    
    return statements


def main():
    sql_file = 'glamstoredb_postgres.sql'
    
    if not os.path.exists(sql_file):
        print(f"✗ Archivo no encontrado: {sql_file}")
        sys.exit(1)
    
    print(f"Leyendo {sql_file}...")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    print("Parseando SQL...")
    statements = parse_sql_statements(sql_content)
    print(f"✓ {len(statements)} statements encontrados")
    
    db_config = settings.DATABASES['default']
    
    print(f"\nConectando a PostgreSQL...")
    print(f"Host: {db_config['HOST']}")
    print(f"BD: {db_config['NAME']}")
    
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
        
        print(f"\nEjecutando {len(statements)} statements...")
        
        for i, statement in enumerate(statements):
            if statement.strip():
                try:
                    cursor.execute(statement)
                    executed += 1
                    
                    # Mostrar progreso cada 50 statements
                    if (i + 1) % 50 == 0:
                        print(f"  ✓ {i + 1}/{len(statements)} statements ejecutados")
                except Exception as e:
                    failed += 1
                    # Mostrar primeros 5 errores
                    if failed <= 5:
                        print(f"  ⚠ Error en statement {i + 1}: {str(e)[:100]}")
                        print(f"    SQL: {statement[:80]}...")
                    pass
        
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
        
        # Contar repartidores
        cursor.execute("SELECT COUNT(*) FROM repartidores;")
        repartidores_count = cursor.fetchone()[0]
        print(f"  - Repartidores: {repartidores_count}")
        
        # Contar notificaciones
        try:
            cursor.execute("SELECT COUNT(*) FROM notificaciones_problema;")
            notificaciones_count = cursor.fetchone()[0]
            print(f"  - Notificaciones: {notificaciones_count}")
        except:
            print(f"  - Notificaciones: tabla no encontrada")
        
        cursor.close()
        conn.close()
        
        print(f"\n✓ Proceso completado exitosamente")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

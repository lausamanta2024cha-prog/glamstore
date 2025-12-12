#!/usr/bin/env python
"""
Script para restaurar BD desde SQL ejecutando directamente en PostgreSQL
Ejecuta: python restore_from_sql.py glamstoredb.sql
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.conf import settings
import psycopg2


def convert_mysql_to_postgres(sql_content):
    """Convertir SQL de MySQL a PostgreSQL"""
    import re
    
    # Reemplazar backticks por comillas dobles
    sql_content = sql_content.replace('`', '"')
    
    # Remover comentarios MySQL especiales (/*!40101 ... */)
    sql_content = re.sub(r'/\*!\d+[^*]*\*/', '', sql_content)
    
    # Remover SET statements de MySQL
    sql_content = re.sub(r'SET\s+SQL_MODE\s*=\s*[^;]*;', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'SET\s+time_zone\s*=\s*[^;]*;', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'SET\s+@OLD_[^;]*;', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'SET\s+NAMES\s+[^;]*;', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'START\s+TRANSACTION;', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'COMMIT;', '', sql_content, flags=re.IGNORECASE)
    
    # Remover ENGINE=InnoDB y similares
    sql_content = re.sub(r'\s+ENGINE=[^\s;]*', '', sql_content, flags=re.IGNORECASE)
    
    # Remover DEFAULT CHARSET
    sql_content = re.sub(r'\s+DEFAULT CHARSET=[^\s;]*', '', sql_content, flags=re.IGNORECASE)
    
    # Remover COLLATE
    sql_content = re.sub(r'\s+COLLATE=[^\s;]*', '', sql_content, flags=re.IGNORECASE)
    
    # Convertir tipos de datos MySQL a PostgreSQL
    sql_content = re.sub(r'\bint\s*\(\d+\)', 'integer', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'\bbigint\s*\(\d+\)', 'bigint', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'\bsmallint\s*\(\d+\)', 'smallint', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'\bvarchar\s*\(', 'character varying(', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'\btinyint\s*\(\d+\)', 'smallint', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'\blongtext\b', 'text', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'\bmediumtext\b', 'text', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'\btext\s*\(\d+\)', 'text', sql_content, flags=re.IGNORECASE)
    
    # Remover UNSIGNED
    sql_content = re.sub(r'\s+UNSIGNED\b', '', sql_content, flags=re.IGNORECASE)
    
    # Remover ON UPDATE current_timestamp()
    sql_content = re.sub(r'\s+ON\s+UPDATE\s+current_timestamp\(\)', '', sql_content, flags=re.IGNORECASE)
    
    # Remover AUTO_INCREMENT (PostgreSQL usa SERIAL)
    sql_content = re.sub(r'\s+AUTO_INCREMENT', '', sql_content, flags=re.IGNORECASE)
    
    # Remover CHECK constraints
    sql_content = re.sub(r',\s*CHECK\s*\([^)]*\)', '', sql_content, flags=re.IGNORECASE)
    
    # Remover KEY constraints que pueden causar problemas
    sql_content = re.sub(r',\s*KEY\s+`[^`]*`\s*\([^)]*\)', '', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r',\s*UNIQUE\s+KEY\s+`[^`]*`\s*\([^)]*\)', '', sql_content, flags=re.IGNORECASE)
    
    # Remover CONSTRAINT FOREIGN KEY
    sql_content = re.sub(r',\s*CONSTRAINT\s+`[^`]*`\s+FOREIGN\s+KEY[^,;]*', '', sql_content, flags=re.IGNORECASE)
    
    # Remover PRIMARY KEY duplicado
    sql_content = re.sub(r',\s*PRIMARY\s+KEY\s*\([^)]*\)', '', sql_content, flags=re.IGNORECASE)
    
    # Limpiar espacios múltiples
    sql_content = re.sub(r'\s+', ' ', sql_content)
    
    return sql_content


def restore_sql_file(sql_file):
    """Restaurar BD desde archivo SQL"""
    
    if not os.path.exists(sql_file):
        print(f"✗ Archivo no encontrado: {sql_file}")
        sys.exit(1)
    
    print(f"Leyendo {sql_file}...")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    print("Convirtiendo SQL de MySQL a PostgreSQL...")
    sql_content = convert_mysql_to_postgres(sql_content)
    
    db_config = settings.DATABASES['default']
    
    print(f"\nConectando a PostgreSQL...")
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
        
        # Ejecutar el SQL completo
        print("Ejecutando SQL...")
        try:
            cursor.execute(sql_content)
            conn.commit()
            print("✓ SQL ejecutado exitosamente")
        except Exception as e:
            print(f"⚠ Error ejecutando SQL: {str(e)[:200]}")
            conn.rollback()
        
        cursor.close()
        conn.close()
        
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
            ('productos', 'Productos'),
            ('clientes', 'Clientes'),
        ]
        
        for table, label in tables_to_check:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM "{table}";')
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"  ✓ {label}: {count}")
                else:
                    print(f"  - {label}: 0")
            except:
                pass
        
        cursor.close()
        conn.close()
        
        print(f"\n✓ Proceso completado")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("RESTAURAR BD DESDE SQL")
    print("=" * 60 + "\n")
    
    sql_file = sys.argv[1] if len(sys.argv) > 1 else 'glamstoredb.sql'
    
    restore_sql_file(sql_file)


if __name__ == '__main__':
    main()

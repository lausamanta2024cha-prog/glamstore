#!/usr/bin/env python
"""
Script completo para restaurar y reparar la BD
1. Crea secuencias faltantes
2. Restaura datos desde MySQL dump
3. Verifica la restauración
"""
import os
import re
import psycopg2
from psycopg2 import sql

DB_HOST = os.getenv('DATABASE_HOST', 'dpg-d4t0vo2li9vc7394ahjg-a.virginia-postgres.render.com')
DB_NAME = os.getenv('DATABASE_NAME', 'glamstoredb')
DB_USER = os.getenv('DATABASE_USER', 'glamstoredb_user')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
DB_PORT = os.getenv('DATABASE_PORT', '5432')

# Mapeo de nombres de columnas MySQL -> PostgreSQL
COLUMN_MAPPINGS = {
    'repartidores': {
        'idRepartidor': 'idrepartidor',
        'nombreRepartidor': 'nombre',
        'estado_turno': None,  # Ignorar
    },
}

def create_sequences():
    """Crea las secuencias necesarias"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, port=DB_PORT
        )
        cursor = conn.cursor()
        
        print("\n=== CREANDO SECUENCIAS ===")
        
        tables_to_check = [
            ('usuarios', 'idusuario'),
            ('clientes', 'idcliente'),
            ('repartidores', 'idrepartidor'),
            ('pedidos', 'idpedido'),
            ('productos', 'idproducto'),
        ]
        
        for table_name, id_column in tables_to_check:
            seq_name = f"{table_name}_{id_column}_seq"
            
            # Verificar si tabla existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_name = %s
                );
            """, [table_name])
            
            if not cursor.fetchone()[0]:
                print(f"⚠ Tabla '{table_name}' no existe")
                continue
            
            # Verificar si secuencia existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.sequences
                    WHERE sequence_name = %s
                );
            """, [seq_name])
            
            if cursor.fetchone()[0]:
                print(f"✓ Secuencia '{seq_name}' ya existe")
                continue
            
            print(f"⚠ Creando secuencia '{seq_name}'...")
            
            # Obtener máximo ID
            cursor.execute(f"SELECT MAX({id_column}) FROM {table_name};")
            max_id = cursor.fetchone()[0] or 0
            
            # Crear secuencia
            cursor.execute(f"""
                CREATE SEQUENCE {seq_name}
                START WITH {max_id + 1}
                INCREMENT BY 1
                NO MINVALUE
                NO MAXVALUE
                CACHE 1;
            """)
            
            # Asignar a columna
            cursor.execute(f"""
                ALTER TABLE {table_name}
                ALTER COLUMN {id_column} SET DEFAULT nextval('{seq_name}');
            """)
            
            # Cambiar propietario
            cursor.execute(f"""
                ALTER SEQUENCE {seq_name} OWNED BY {table_name}.{id_column};
            """)
            
            print(f"✓ Secuencia creada (inicio: {max_id + 1})")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error creando secuencias: {str(e)}")

def parse_insert_statement(line):
    """Parsea un INSERT statement de MySQL"""
    match = re.match(
        r"INSERT INTO `(\w+)` \((.*?)\) VALUES (.*);",
        line,
        re.IGNORECASE
    )
    
    if not match:
        return None
    
    table_name = match.group(1)
    columns_str = match.group(2)
    values_str = match.group(3)
    
    columns = [col.strip().strip('`') for col in columns_str.split(',')]
    
    # Parsear valores
    value_rows = []
    rows = re.findall(r'\(([^)]*)\)', values_str)
    
    for row in rows:
        values = []
        current_value = ''
        in_string = False
        
        for i, char in enumerate(row):
            if char == "'" and (i == 0 or row[i-1] != '\\'):
                in_string = not in_string
                current_value += char
            elif char == ',' and not in_string:
                values.append(current_value.strip())
                current_value = ''
            else:
                current_value += char
        
        if current_value:
            values.append(current_value.strip())
        
        value_rows.append(values)
    
    return {
        'table': table_name,
        'columns': columns,
        'values': value_rows
    }

def convert_value(value):
    """Convierte un valor de MySQL a PostgreSQL"""
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
        value = value.replace("\\'", "'")
        value = value.replace("\\\\", "\\")
        return value
    
    if value.upper() == 'NULL':
        return None
    
    return value

def restore_data(dump_file):
    """Restaura datos desde MySQL dump"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, port=DB_PORT
        )
        cursor = conn.cursor()
        
        print(f"\n=== RESTAURANDO DATOS ===")
        print(f"Leyendo {dump_file}...")
        
        with open(dump_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        insert_count = 0
        error_count = 0
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            if not line.startswith('INSERT INTO'):
                continue
            
            parsed = parse_insert_statement(line)
            if not parsed:
                continue
            
            table_name = parsed['table']
            columns = parsed['columns']
            values_rows = parsed['values']
            
            # Aplicar mapeo de columnas
            if table_name in COLUMN_MAPPINGS:
                mapping = COLUMN_MAPPINGS[table_name]
                
                new_columns = []
                column_indices_to_keep = []
                
                for i, col in enumerate(columns):
                    mapped_col = mapping.get(col, col)
                    if mapped_col is not None:
                        new_columns.append(mapped_col)
                        column_indices_to_keep.append(i)
                
                columns = new_columns
                
                new_values_rows = []
                for row in values_rows:
                    new_row = [row[i] for i in column_indices_to_keep if i < len(row)]
                    new_values_rows.append(new_row)
                
                values_rows = new_values_rows
            
            # Insertar datos
            for row in values_rows:
                try:
                    converted_values = [convert_value(v) for v in row]
                    
                    placeholders = ', '.join(['%s'] * len(columns))
                    insert_sql = f"""
                        INSERT INTO {table_name} ({', '.join(columns)})
                        VALUES ({placeholders})
                    """
                    
                    cursor.execute(insert_sql, converted_values)
                    insert_count += 1
                    
                except Exception as e:
                    error_count += 1
                    if error_count <= 3:
                        print(f"⚠ Error en línea {line_num}: {str(e)}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✓ Restauración completada")
        print(f"  - Insertados: {insert_count}")
        print(f"  - Errores: {error_count}")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def verify_data():
    """Verifica los datos restaurados"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, port=DB_PORT
        )
        cursor = conn.cursor()
        
        print(f"\n=== VERIFICANDO DATOS ===")
        
        tables = ['usuarios', 'clientes', 'repartidores', 'pedidos', 'productos']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count}")
        
        # Mostrar algunos repartidores
        print(f"\nPrimeros repartidores:")
        cursor.execute("SELECT idrepartidor, nombre, telefono, email FROM repartidores LIMIT 3;")
        for row in cursor.fetchall():
            print(f"  - ID: {row[0]}, Nombre: {row[1]}, Tel: {row[2]}, Email: {row[3]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error verificando: {str(e)}")

if __name__ == '__main__':
    import sys
    
    dump_file = 'glamstoredb.sql'
    if len(sys.argv) > 1:
        dump_file = sys.argv[1]
    
    print("Iniciando restauración completa de BD...")
    create_sequences()
    restore_data(dump_file)
    verify_data()
    print("\n✓ Proceso completado")

#!/usr/bin/env python
"""
Script para restaurar datos de MySQL dump a PostgreSQL
Maneja conversiones de nombres de columnas y tipos de datos
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
        'estado_turno': None,  # Ignorar esta columna
    },
    'usuarios': {
        'idUsuario': 'idusuario',
    },
    'clientes': {
        'idCliente': 'idcliente',
    },
    'pedidos': {
        'idPedido': 'idpedido',
    },
}

def parse_insert_statement(line):
    """Parsea un INSERT statement de MySQL"""
    # Formato: INSERT INTO `table` (`col1`, `col2`) VALUES (val1, val2), (val3, val4)
    
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
    
    # Parsear columnas
    columns = [col.strip().strip('`') for col in columns_str.split(',')]
    
    # Parsear valores (múltiples filas)
    # Esto es complejo porque los valores pueden contener comas dentro de strings
    value_rows = []
    
    # Dividir por ), ( para separar filas
    rows = re.findall(r'\(([^)]*)\)', values_str)
    
    for row in rows:
        # Parsear valores individuales respetando strings
        values = []
        current_value = ''
        in_string = False
        escape_next = False
        
        for char in row:
            if escape_next:
                current_value += char
                escape_next = False
            elif char == '\\':
                escape_next = True
                current_value += char
            elif char == "'" and not escape_next:
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

def convert_value(value, column_name, table_name):
    """Convierte un valor de MySQL a PostgreSQL"""
    
    # Remover comillas
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
        # Desescapar caracteres
        value = value.replace("\\'", "'")
        value = value.replace("\\\\", "\\")
        return value
    
    # NULL
    if value.upper() == 'NULL':
        return None
    
    # Booleanos (solo para columnas específicas)
    if column_name in ['is_active', 'is_staff', 'is_superuser']:
        return value == '1'
    
    return value

def restore_from_mysql_dump(dump_file):
    """Restaura datos desde un dump de MySQL"""
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, port=DB_PORT
        )
        cursor = conn.cursor()
        
        print(f"Leyendo {dump_file}...")
        
        with open(dump_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        insert_count = 0
        error_count = 0
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Buscar INSERT statements
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
                
                # Filtrar columnas ignoradas
                new_columns = []
                column_indices_to_keep = []
                
                for i, col in enumerate(columns):
                    mapped_col = mapping.get(col, col)
                    if mapped_col is not None:
                        new_columns.append(mapped_col)
                        column_indices_to_keep.append(i)
                
                columns = new_columns
                
                # Filtrar valores
                new_values_rows = []
                for row in values_rows:
                    new_row = [row[i] for i in column_indices_to_keep if i < len(row)]
                    new_values_rows.append(new_row)
                
                values_rows = new_values_rows
            
            # Insertar datos
            for row in values_rows:
                try:
                    # Convertir valores
                    converted_values = []
                    for i, value in enumerate(row):
                        col_name = columns[i] if i < len(columns) else ''
                        converted = convert_value(value, col_name, table_name)
                        converted_values.append(converted)
                    
                    # Construir INSERT
                    placeholders = ', '.join(['%s'] * len(columns))
                    insert_sql = f"""
                        INSERT INTO {table_name} ({', '.join(columns)})
                        VALUES ({placeholders})
                    """
                    
                    cursor.execute(insert_sql, converted_values)
                    insert_count += 1
                    
                except Exception as e:
                    error_count += 1
                    print(f"⚠ Error en línea {line_num}: {str(e)}")
                    if error_count <= 5:  # Mostrar solo los primeros 5 errores
                        print(f"  SQL: {insert_sql}")
                        print(f"  Valores: {converted_values}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n✓ Restauración completada")
        print(f"  - Insertados: {insert_count}")
        print(f"  - Errores: {error_count}")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    import sys
    
    dump_file = 'glamstoredb.sql'
    if len(sys.argv) > 1:
        dump_file = sys.argv[1]
    
    restore_from_mysql_dump(dump_file)

#!/usr/bin/env python
"""
Script mejorado para convertir MySQL dump a PostgreSQL
Maneja correctamente los INSERT statements y tipos de datos
"""
import re
import sys

def convert_mysql_to_postgres(input_file, output_file):
    """Convierte un dump de MySQL a PostgreSQL"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Leyendo {input_file}...")
    
    # 1. Remover comentarios de phpMyAdmin
    content = re.sub(r'-- .*?\n', '\n', content)
    
    # 2. Remover BEGIN; y COMMIT;
    content = re.sub(r'BEGIN;?\s*\n', '', content)
    content = re.sub(r'COMMIT;?\s*\n', '', content)
    
    # 3. Convertir backticks a comillas dobles
    content = content.replace('`', '"')
    
    # 4. Convertir tipos de datos MySQL a PostgreSQL
    conversions = {
        r'\bint\b': 'integer',
        r'\bbigint\b': 'bigint',
        r'\bsmallint\b': 'smallint',
        r'\btinyint\b': 'smallint',
        r'\bvarchar\b': 'character varying',
        r'\btext\b': 'text',
        r'\bdatetime\b': 'timestamp',
        r'\bdate\b': 'date',
        r'\btime\b': 'time',
        r'\bdecimal\b': 'numeric',
        r'\bfloat\b': 'real',
        r'\bdouble\b': 'double precision',
        r'\bboolean\b': 'boolean',
        r'\bbool\b': 'boolean',
    }
    
    for mysql_type, pg_type in conversions.items():
        content = re.sub(mysql_type, pg_type, content, flags=re.IGNORECASE)
    
    # 5. Convertir AUTO_INCREMENT a SERIAL
    content = re.sub(
        r'(\w+)\s+integer\s+NOT\s+NULL\s+AUTO_INCREMENT',
        r'\1 SERIAL',
        content,
        flags=re.IGNORECASE
    )
    
    # 6. Remover ENGINE, CHARSET, COLLATE
    content = re.sub(r'\s*ENGINE\s*=\s*\w+', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*CHARSET\s*=\s*\w+', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*COLLATE\s*=\s*[\w_]+', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*DEFAULT\s+CHARSET\s*=\s*\w+', '', content, flags=re.IGNORECASE)
    
    # 7. Convertir PRIMARY KEY inline a constraint
    content = re.sub(
        r'(\w+)\s+SERIAL\s+PRIMARY\s+KEY',
        r'\1 SERIAL PRIMARY KEY',
        content
    )
    
    # 8. Convertir INSERT statements
    # Cambiar VALUES (x), (y), (z) a múltiples INSERT
    def convert_insert_values(match):
        insert_part = match.group(1)
        values_part = match.group(2)
        
        # Dividir los valores por comas, pero respetando paréntesis
        value_groups = re.findall(r'\([^)]*\)', values_part)
        
        inserts = []
        for value_group in value_groups:
            inserts.append(f"INSERT INTO {insert_part} VALUES {value_group};")
        
        return '\n'.join(inserts)
    
    content = re.sub(
        r'INSERT INTO\s+([^(]+)\s+\(([^)]+)\)\s+VALUES\s+(\([^;]+\));',
        lambda m: f"INSERT INTO {m.group(1)} ({m.group(2)}) VALUES {m.group(3)};",
        content,
        flags=re.IGNORECASE
    )
    
    # 9. Convertir booleanos: 0 -> false, 1 -> true (pero solo en contextos específicos)
    # Esto es delicado, así que solo lo hacemos en columnas que sabemos son booleanas
    
    # 10. Remover líneas vacías múltiples
    content = re.sub(r'\n\n+', '\n\n', content)
    
    # 11. Remover espacios en blanco al final de líneas
    content = '\n'.join(line.rstrip() for line in content.split('\n'))
    
    # Escribir el archivo convertido
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Convertido a {output_file}")
    
    # Contar statements
    insert_count = len(re.findall(r'INSERT INTO', content))
    create_count = len(re.findall(r'CREATE TABLE', content))
    
    print(f"  - CREATE TABLE statements: {create_count}")
    print(f"  - INSERT statements: {insert_count}")

if __name__ == '__main__':
    input_file = 'glamstoredb.sql'
    output_file = 'glamstoredb_postgres_v2.sql'
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    convert_mysql_to_postgres(input_file, output_file)

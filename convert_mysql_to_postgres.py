#!/usr/bin/env python
"""
Script para convertir SQL de MySQL a PostgreSQL
Uso: python convert_mysql_to_postgres.py glamstoredb.sql
"""
import sys
import re


def convert_mysql_to_postgres(sql_content):
    """Convertir SQL de MySQL a PostgreSQL"""
    
    # 1. Reemplazar ENGINE=InnoDB por nada (PostgreSQL no lo necesita)
    sql_content = re.sub(r'\s+ENGINE=InnoDB[^;]*', '', sql_content, flags=re.IGNORECASE)
    
    # 2. Reemplazar DEFAULT CHARSET por nada
    sql_content = re.sub(r'\s+DEFAULT CHARSET=[^\s;]*', '', sql_content, flags=re.IGNORECASE)
    
    # 3. Reemplazar COLLATE por nada
    sql_content = re.sub(r'\s+COLLATE=[^\s;]*', '', sql_content, flags=re.IGNORECASE)
    
    # 4. Reemplazar AUTO_INCREMENT por SERIAL
    sql_content = re.sub(r'\bAUTO_INCREMENT\b', 'SERIAL', sql_content, flags=re.IGNORECASE)
    
    # 5. Reemplazar backticks por comillas dobles
    sql_content = sql_content.replace('`', '"')
    
    # 6. Reemplazar int(11) por integer
    sql_content = re.sub(r'\bint\s*\(\d+\)', 'integer', sql_content, flags=re.IGNORECASE)
    
    # 7. Reemplazar bigint(20) por bigint
    sql_content = re.sub(r'\bbigint\s*\(\d+\)', 'bigint', sql_content, flags=re.IGNORECASE)
    
    # 8. Reemplazar varchar(X) por character varying(X)
    sql_content = re.sub(r'\bvarchar\s*\(', 'character varying(', sql_content, flags=re.IGNORECASE)
    
    # 9. Reemplazar tinyint por smallint
    sql_content = re.sub(r'\btinyint\s*\(\d+\)', 'smallint', sql_content, flags=re.IGNORECASE)
    
    # 10. Reemplazar UNSIGNED por nada (PostgreSQL maneja esto diferente)
    sql_content = re.sub(r'\bUNSIGNED\b', '', sql_content, flags=re.IGNORECASE)
    
    # 11. Reemplazar PRIMARY KEY AUTO_INCREMENT por PRIMARY KEY SERIAL
    sql_content = re.sub(
        r'(\w+)\s+integer\s+NOT NULL\s+AUTO_INCREMENT',
        r'\1 SERIAL',
        sql_content,
        flags=re.IGNORECASE
    )
    
    # 12. Reemplazar CONSTRAINT ... FOREIGN KEY por ALTER TABLE
    # Esto es más complejo, lo dejamos para después
    
    # 13. Limpiar espacios múltiples
    sql_content = re.sub(r'\s+', ' ', sql_content)
    
    return sql_content


def main():
    if len(sys.argv) < 2:
        print("Uso: python convert_mysql_to_postgres.py <archivo_sql>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = input_file.replace('.sql', '_postgres.sql')
    
    print(f"Leyendo {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
    except Exception as e:
        print(f"✗ Error leyendo archivo: {e}")
        sys.exit(1)
    
    print("Convirtiendo SQL de MySQL a PostgreSQL...")
    converted = convert_mysql_to_postgres(sql_content)
    
    print(f"Escribiendo {output_file}...")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted)
    except Exception as e:
        print(f"✗ Error escribiendo archivo: {e}")
        sys.exit(1)
    
    print(f"✓ Conversión completada")
    print(f"✓ Archivo generado: {output_file}")
    print(f"\nPróximos pasos:")
    print(f"1. Revisa el archivo {output_file}")
    print(f"2. Sube a GitHub: git add {output_file}")
    print(f"3. En Render ejecuta: python manage.py populate_data {output_file}")


if __name__ == '__main__':
    main()

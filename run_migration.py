#!/usr/bin/env python
"""
Script para agregar la columna email a la tabla repartidores
Ejecutar con: python run_migration.py
"""

import subprocess
import sys

# Intentar ejecutar la migración
print("Ejecutando migraciones...")
result = subprocess.run([sys.executable, "manage.py", "migrate", "core", "0014_repartidor_email"], 
                       capture_output=True, text=True, timeout=30)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

if result.returncode == 0:
    print("\n✓ Migración ejecutada exitosamente")
else:
    print("\n✗ Error en la migración")
    print("\nIntentando agregar la columna directamente...")
    
    # Intentar agregar la columna directamente
    import pymysql
    try:
        conn = pymysql.connect(host='localhost', user='root', password='', database='glamstoredb')
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE repartidores ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL")
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Columna agregada exitosamente")
    except Exception as e:
        print(f"✗ Error: {e}")

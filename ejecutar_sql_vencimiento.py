#!/usr/bin/env python
"""
Script para agregar la columna fechaVencimiento a la tabla pedidos
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.db import connection

print('=== AGREGANDO COLUMNA fechaVencimiento ===')
print()

try:
    with connection.cursor() as cursor:
        # Verificar si la columna ya existe
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='pedidos' AND COLUMN_NAME='fechaVencimiento'
        """)
        
        if cursor.fetchone():
            print("✓ La columna fechaVencimiento ya existe")
        else:
            print("Agregando columna fechaVencimiento...")
            cursor.execute("""
                ALTER TABLE pedidos ADD COLUMN fechaVencimiento DATE NULL
            """)
            print("✓ Columna agregada exitosamente")
            
            # Crear índice
            print("Creando índice...")
            cursor.execute("""
                CREATE INDEX idx_fecha_vencimiento ON pedidos(fechaVencimiento)
            """)
            print("✓ Índice creado exitosamente")
    
    print()
    print("✅ Base de datos actualizada correctamente")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

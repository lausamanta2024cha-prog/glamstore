#!/usr/bin/env python
import os
import django
import pymysql

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.db import connection

# Ejecutar el SQL para agregar la columna
try:
    with connection.cursor() as cursor:
        # Verificar si la columna ya existe
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'repartidores' 
            AND COLUMN_NAME = 'email'
        """)
        
        if cursor.fetchone():
            print("La columna 'email' ya existe en la tabla 'repartidores'")
        else:
            # Agregar la columna
            cursor.execute("""
                ALTER TABLE repartidores 
                ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL
            """)
            print("Columna 'email' agregada exitosamente a la tabla 'repartidores'")
            
except Exception as e:
    print(f"Error: {e}")

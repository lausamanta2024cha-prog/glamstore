#!/usr/bin/env python
"""
Script para verificar y reparar todos los problemas de la BD
"""
import os
import psycopg2
from psycopg2 import sql

DB_HOST = os.getenv('DATABASE_HOST', 'dpg-d4t0vo2li9vc7394ahjg-a.virginia-postgres.render.com')
DB_NAME = os.getenv('DATABASE_NAME', 'glamstoredb')
DB_USER = os.getenv('DATABASE_USER', 'glamstoredb_user')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
DB_PORT = os.getenv('DATABASE_PORT', '5432')

def check_and_fix_sequences():
    """Verifica y crea las secuencias necesarias"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, port=DB_PORT
        )
        cursor = conn.cursor()
        
        print("\n=== VERIFICANDO SECUENCIAS ===")
        
        # Tablas que necesitan secuencias
        tables_to_check = [
            ('usuarios', 'idusuario'),
            ('clientes', 'idcliente'),
            ('repartidores', 'idrepartidor'),
            ('pedidos', 'idpedido'),
            ('productos', 'idproducto'),
        ]
        
        for table_name, id_column in tables_to_check:
            seq_name = f"{table_name}_{id_column}_seq"
            
            # Verificar si la tabla existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_name = %s
                );
            """, [table_name])
            
            table_exists = cursor.fetchone()[0]
            if not table_exists:
                print(f"⚠ Tabla '{table_name}' no existe")
                continue
            
            # Verificar si la secuencia existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.sequences
                    WHERE sequence_name = %s
                );
            """, [seq_name])
            
            seq_exists = cursor.fetchone()[0]
            
            if not seq_exists:
                print(f"⚠ Secuencia '{seq_name}' NO existe. Creando...")
                
                # Obtener el máximo ID
                cursor.execute(f"SELECT MAX({id_column}) FROM {table_name};")
                max_id = cursor.fetchone()[0] or 0
                
                # Crear la secuencia
                cursor.execute(f"""
                    CREATE SEQUENCE {seq_name}
                    START WITH {max_id + 1}
                    INCREMENT BY 1
                    NO MINVALUE
                    NO MAXVALUE
                    CACHE 1;
                """)
                
                # Asignar a la columna
                cursor.execute(f"""
                    ALTER TABLE {table_name}
                    ALTER COLUMN {id_column} SET DEFAULT nextval('{seq_name}');
                """)
                
                # Cambiar propietario
                cursor.execute(f"""
                    ALTER SEQUENCE {seq_name} OWNED BY {table_name}.{id_column};
                """)
                
                print(f"✓ Secuencia '{seq_name}' creada (inicio: {max_id + 1})")
            else:
                print(f"✓ Secuencia '{seq_name}' existe")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error en secuencias: {str(e)}")

def check_table_structure():
    """Verifica la estructura de las tablas principales"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, port=DB_PORT
        )
        cursor = conn.cursor()
        
        print("\n=== VERIFICANDO ESTRUCTURA DE TABLAS ===")
        
        # Verificar tabla usuarios
        print("\nTabla 'usuarios':")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'usuarios'
            ORDER BY ordinal_position;
        """)
        
        for col in cursor.fetchall():
            print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")
        
        # Verificar tabla repartidores
        print("\nTabla 'repartidores':")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'repartidores'
            ORDER BY ordinal_position;
        """)
        
        for col in cursor.fetchall():
            print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error verificando estructura: {str(e)}")

def check_data_counts():
    """Verifica la cantidad de datos en las tablas principales"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, port=DB_PORT
        )
        cursor = conn.cursor()
        
        print("\n=== CONTEO DE DATOS ===")
        
        tables = ['usuarios', 'clientes', 'repartidores', 'pedidos', 'productos', 'roles']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error contando datos: {str(e)}")

if __name__ == '__main__':
    print("Iniciando verificación y reparación de BD...")
    check_and_fix_sequences()
    check_table_structure()
    check_data_counts()
    print("\n✓ Verificación completada")

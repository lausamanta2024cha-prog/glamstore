#!/usr/bin/env python
"""
Script para verificar y reparar la secuencia de idusuario en PostgreSQL
"""
import os
import psycopg2
from psycopg2 import sql

# Obtener credenciales de la BD desde variables de entorno
DB_HOST = os.getenv('DATABASE_HOST', 'dpg-d4t0vo2li9vc7394ahjg-a.virginia-postgres.render.com')
DB_NAME = os.getenv('DATABASE_NAME', 'glamstoredb')
DB_USER = os.getenv('DATABASE_USER', 'glamstoredb_user')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
DB_PORT = os.getenv('DATABASE_PORT', '5432')

try:
    print("Conectando a PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()
    
    print("\n1. Verificando estructura de la tabla 'usuarios'...")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'usuarios'
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    print("\nColumnas en la tabla 'usuarios':")
    for col in columns:
        print(f"  - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
    
    print("\n2. Verificando secuencias existentes...")
    cursor.execute("""
        SELECT sequence_name
        FROM information_schema.sequences
        WHERE sequence_schema = 'public';
    """)
    
    sequences = cursor.fetchall()
    print(f"\nSecuencias encontradas: {len(sequences)}")
    for seq in sequences:
        print(f"  - {seq[0]}")
    
    print("\n3. Verificando si existe secuencia para idusuario...")
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.sequences
            WHERE sequence_name = 'usuarios_idusuario_seq'
        );
    """)
    
    seq_exists = cursor.fetchone()[0]
    
    if not seq_exists:
        print("⚠ Secuencia 'usuarios_idusuario_seq' NO existe. Creando...")
        
        # Obtener el máximo ID actual
        cursor.execute("SELECT MAX(idusuario) FROM usuarios;")
        max_id = cursor.fetchone()[0] or 0
        print(f"  ID máximo actual: {max_id}")
        
        # Crear la secuencia
        cursor.execute(f"""
            CREATE SEQUENCE usuarios_idusuario_seq
            START WITH {max_id + 1}
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1;
        """)
        
        # Asignar la secuencia a la columna
        cursor.execute("""
            ALTER TABLE usuarios
            ALTER COLUMN idusuario SET DEFAULT nextval('usuarios_idusuario_seq');
        """)
        
        # Cambiar el propietario de la secuencia
        cursor.execute("""
            ALTER SEQUENCE usuarios_idusuario_seq OWNED BY usuarios.idusuario;
        """)
        
        conn.commit()
        print("✓ Secuencia creada y asignada exitosamente")
    else:
        print("✓ Secuencia 'usuarios_idusuario_seq' ya existe")
    
    print("\n4. Verificando datos en la tabla 'usuarios'...")
    cursor.execute("SELECT COUNT(*) FROM usuarios;")
    count = cursor.fetchone()[0]
    print(f"  Total de usuarios: {count}")
    
    if count > 0:
        cursor.execute("SELECT idusuario, email, nombre FROM usuarios LIMIT 5;")
        users = cursor.fetchall()
        print("  Primeros 5 usuarios:")
        for user in users:
            print(f"    - ID: {user[0]}, Email: {user[1]}, Nombre: {user[2]}")
    
    print("\n✓ Verificación completada")
    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()

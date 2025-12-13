#!/usr/bin/env python
"""
Script para ejecutar en Render
Restaura la BD completa desde glamstoredb.sql
"""
import os
import sys
import re
import psycopg2
from psycopg2 import sql

# Credenciales de BD
DB_HOST = os.getenv('DATABASE_HOST', 'dpg-d4t0vo2li9vc7394ahjg-a.virginia-postgres.render.com')
DB_NAME = os.getenv('DATABASE_NAME', 'glamstoredb')
DB_USER = os.getenv('DATABASE_USER', 'glamstoredb_user')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
DB_PORT = os.getenv('DATABASE_PORT', '5432')

# Mapeo de columnas MySQL -> PostgreSQL
COLUMN_MAPPINGS = {
    'repartidores': {
        'idRepartidor': 'idrepartidor',
        'nombreRepartidor': 'nombre',
        'estado_turno': None,  # Ignorar
    },
}

def conectar_bd():
    """Conecta a la BD"""
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER,
        password=DB_PASSWORD, port=DB_PORT
    )

def crear_secuencias():
    """Crea las secuencias necesarias en PostgreSQL"""
    print("\n" + "="*50)
    print("PASO 1: CREANDO SECUENCIAS")
    print("="*50)
    
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        tablas = [
            ('usuarios', 'idusuario'),
            ('clientes', 'idcliente'),
            ('repartidores', 'idrepartidor'),
            ('pedidos', 'idpedido'),
            ('productos', 'idproducto'),
        ]
        
        for tabla, columna_id in tablas:
            nombre_seq = f"{tabla}_{columna_id}_seq"
            
            # Verificar si tabla existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_name = %s
                );
            """, [tabla])
            
            if not cursor.fetchone()[0]:
                print(f"⚠ Tabla '{tabla}' no existe")
                continue
            
            # Verificar si secuencia existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.sequences
                    WHERE sequence_name = %s
                );
            """, [nombre_seq])
            
            if cursor.fetchone()[0]:
                print(f"✓ Secuencia '{nombre_seq}' ya existe")
                continue
            
            print(f"⚠ Creando secuencia '{nombre_seq}'...")
            
            # Obtener máximo ID
            cursor.execute(f"SELECT MAX({columna_id}) FROM {tabla};")
            max_id = cursor.fetchone()[0] or 0
            
            # Crear secuencia
            cursor.execute(f"""
                CREATE SEQUENCE {nombre_seq}
                START WITH {max_id + 1}
                INCREMENT BY 1
                NO MINVALUE
                NO MAXVALUE
                CACHE 1;
            """)
            
            # Asignar a columna
            cursor.execute(f"""
                ALTER TABLE {tabla}
                ALTER COLUMN {columna_id} SET DEFAULT nextval('{nombre_seq}');
            """)
            
            # Cambiar propietario
            cursor.execute(f"""
                ALTER SEQUENCE {nombre_seq} OWNED BY {tabla}.{columna_id};
            """)
            
            print(f"✓ Secuencia creada (inicio: {max_id + 1})")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Secuencias creadas exitosamente")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False
    
    return True

def parsear_insert(linea):
    """Parsea un INSERT statement de MySQL"""
    match = re.match(
        r"INSERT INTO `(\w+)` \((.*?)\) VALUES (.*);",
        linea,
        re.IGNORECASE
    )
    
    if not match:
        return None
    
    tabla = match.group(1)
    columnas_str = match.group(2)
    valores_str = match.group(3)
    
    columnas = [col.strip().strip('`') for col in columnas_str.split(',')]
    
    # Parsear valores
    filas_valores = []
    filas = re.findall(r'\(([^)]*)\)', valores_str)
    
    for fila in filas:
        valores = []
        valor_actual = ''
        en_string = False
        
        for i, char in enumerate(fila):
            if char == "'" and (i == 0 or fila[i-1] != '\\'):
                en_string = not en_string
                valor_actual += char
            elif char == ',' and not en_string:
                valores.append(valor_actual.strip())
                valor_actual = ''
            else:
                valor_actual += char
        
        if valor_actual:
            valores.append(valor_actual.strip())
        
        filas_valores.append(valores)
    
    return {
        'tabla': tabla,
        'columnas': columnas,
        'valores': filas_valores
    }

def convertir_valor(valor):
    """Convierte un valor de MySQL a PostgreSQL"""
    if valor.startswith("'") and valor.endswith("'"):
        valor = valor[1:-1]
        valor = valor.replace("\\'", "'")
        valor = valor.replace("\\\\", "\\")
        return valor
    
    if valor.upper() == 'NULL':
        return None
    
    return valor

def restaurar_datos(archivo_dump):
    """Restaura datos desde el dump de MySQL"""
    print("\n" + "="*50)
    print("PASO 2: RESTAURANDO DATOS")
    print("="*50)
    
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        print(f"Leyendo {archivo_dump}...")
        
        with open(archivo_dump, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        insertados = 0
        errores = 0
        
        for num_linea, linea in enumerate(lineas, 1):
            linea = linea.strip()
            
            if not linea.startswith('INSERT INTO'):
                continue
            
            parseado = parsear_insert(linea)
            if not parseado:
                continue
            
            tabla = parseado['tabla']
            columnas = parseado['columnas']
            filas_valores = parseado['valores']
            
            # Aplicar mapeo de columnas
            if tabla in COLUMN_MAPPINGS:
                mapeo = COLUMN_MAPPINGS[tabla]
                
                nuevas_columnas = []
                indices_a_mantener = []
                
                for i, col in enumerate(columnas):
                    col_mapeada = mapeo.get(col, col)
                    if col_mapeada is not None:
                        nuevas_columnas.append(col_mapeada)
                        indices_a_mantener.append(i)
                
                columnas = nuevas_columnas
                
                nuevas_filas = []
                for fila in filas_valores:
                    nueva_fila = [fila[i] for i in indices_a_mantener if i < len(fila)]
                    nuevas_filas.append(nueva_fila)
                
                filas_valores = nuevas_filas
            
            # Insertar datos
            for fila in filas_valores:
                try:
                    valores_convertidos = [convertir_valor(v) for v in fila]
                    
                    placeholders = ', '.join(['%s'] * len(columnas))
                    sql_insert = f"""
                        INSERT INTO {tabla} ({', '.join(columnas)})
                        VALUES ({placeholders})
                    """
                    
                    cursor.execute(sql_insert, valores_convertidos)
                    insertados += 1
                    
                except Exception as e:
                    errores += 1
                    if errores <= 3:
                        print(f"⚠ Error en línea {num_linea}: {str(e)}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✓ Restauración completada")
        print(f"  - Insertados: {insertados}")
        print(f"  - Errores: {errores}")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False
    
    return True

def verificar_datos():
    """Verifica los datos restaurados"""
    print("\n" + "="*50)
    print("PASO 3: VERIFICANDO DATOS")
    print("="*50)
    
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        tablas = ['usuarios', 'clientes', 'repartidores', 'pedidos', 'productos']
        
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla};")
            cantidad = cursor.fetchone()[0]
            print(f"  {tabla}: {cantidad}")
        
        # Mostrar algunos repartidores
        print(f"\nPrimeros repartidores:")
        cursor.execute("SELECT idrepartidor, nombre, telefono, email FROM repartidores LIMIT 3;")
        for fila in cursor.fetchall():
            print(f"  - ID: {fila[0]}, Nombre: {fila[1]}, Tel: {fila[2]}, Email: {fila[3]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    import os
    
    archivo_dump = 'glamstoredb.sql'
    if len(sys.argv) > 1:
        archivo_dump = sys.argv[1]
    
    print("\n" + "="*50)
    print("RESTAURACIÓN COMPLETA DE BD")
    print("="*50)
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo_dump):
        print(f"✗ Archivo '{archivo_dump}' no encontrado")
        print(f"  Directorio actual: {os.getcwd()}")
        print(f"  Archivos disponibles: {os.listdir('.')[:10]}")
        sys.exit(1)
    
    print(f"✓ Archivo '{archivo_dump}' encontrado")
    
    if not crear_secuencias():
        print("✗ Error creando secuencias")
        sys.exit(1)
    
    if not restaurar_datos(archivo_dump):
        print("✗ Error restaurando datos")
        sys.exit(1)
    
    if not verificar_datos():
        print("✗ Error verificando datos")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("✓ RESTAURACIÓN COMPLETADA EXITOSAMENTE")
    print("="*50)

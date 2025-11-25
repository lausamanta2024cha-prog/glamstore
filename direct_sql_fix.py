import pymysql

# Conectar a la base de datos
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='glamstoredb'
)

try:
    with connection.cursor() as cursor:
        # Verificar si la columna existe
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'repartidores' 
            AND COLUMN_NAME = 'email'
        """)
        
        if cursor.fetchone():
            print("La columna 'email' ya existe")
        else:
            # Agregar la columna
            cursor.execute("""
                ALTER TABLE repartidores 
                ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL
            """)
            connection.commit()
            print("Columna 'email' agregada exitosamente")
finally:
    connection.close()

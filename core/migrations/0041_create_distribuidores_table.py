# Generated migration to create distribuidores table using raw SQL

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_create_correos_pendientes_table'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS distribuidores (
                "idDistribuidor" SERIAL PRIMARY KEY,
                "nombreDistribuidor" varchar(30) NULL,
                "contacto" varchar(100) NULL,
                "telefono" varchar(20) NULL,
                "email" varchar(254) NULL,
                "direccion" varchar(255) NULL
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS distribuidores CASCADE;",
            state_operations=[]
        ),
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS distribuidor_producto (
                "id" SERIAL PRIMARY KEY,
                "idDistribuidor" integer NOT NULL,
                "idProducto" integer NOT NULL,
                "precioCompra" numeric(10, 2) NOT NULL
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS distribuidor_producto CASCADE;",
            state_operations=[]
        ),
    ]

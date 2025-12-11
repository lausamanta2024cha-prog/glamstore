# Generated migration to create configuracion_global table

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_create_all_tables'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS configuracion_global (
                id BIGSERIAL PRIMARY KEY,
                margen_ganancia DECIMAL(5, 2) DEFAULT 10.00,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS configuracion_global CASCADE;",
        ),
        migrations.RunSQL(
            sql="INSERT INTO configuracion_global (id, margen_ganancia, fecha_actualizacion) VALUES (1, 10.00, CURRENT_TIMESTAMP) ON CONFLICT DO NOTHING;",
            reverse_sql="DELETE FROM configuracion_global WHERE id = 1;",
        ),
    ]

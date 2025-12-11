# Generated migration to fix fecha_vencimiento column name in pedidos table

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_fix_pedidos_fecha_vencimiento_column'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'pedidos' AND column_name = 'fecha_vencimiento'
                ) THEN
                    ALTER TABLE pedidos RENAME COLUMN fecha_vencimiento TO fechavencimiento;
                END IF;
            END $$;
            """,
            reverse_sql="""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'pedidos' AND column_name = 'fechavencimiento'
                ) THEN
                    ALTER TABLE pedidos RENAME COLUMN fechavencimiento TO fecha_vencimiento;
                END IF;
            END $$;
            """,
        ),
    ]

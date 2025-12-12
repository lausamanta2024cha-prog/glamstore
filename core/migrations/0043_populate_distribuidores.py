# Generated migration to populate distribuidores table

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_populate_lotes_and_vencimiento'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            INSERT INTO distribuidores ("idDistribuidor", "nombreDistribuidor", "contacto") 
            VALUES 
            (1, 'Proveedor Central', '214748364'),
            (7, 'Proveedor Central tt', '214748364755')
            ON CONFLICT ("idDistribuidor") DO NOTHING;
            """,
            reverse_sql="DELETE FROM distribuidores WHERE \"idDistribuidor\" IN (1, 7);",
            state_operations=[]
        ),
    ]

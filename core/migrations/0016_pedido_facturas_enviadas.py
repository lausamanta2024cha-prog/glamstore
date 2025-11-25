# Generated migration for adding facturas_enviadas field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_repartidor_telefono'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE pedidos ADD COLUMN facturasEnviadas INT DEFAULT 0 NOT NULL;",
            reverse_sql="ALTER TABLE pedidos DROP COLUMN facturasEnviadas;",
        ),
    ]

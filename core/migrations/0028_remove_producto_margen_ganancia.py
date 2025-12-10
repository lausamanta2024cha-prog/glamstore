# Generated migration to remove margen_ganancia from producto

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_configuracion_global'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='margen_ganancia',
        ),
    ]

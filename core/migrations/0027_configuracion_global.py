# Generated migration to add configuracion_global table

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_producto_margen_ganancia'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionGlobal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('margen_ganancia', models.DecimalField(decimal_places=2, default=10, help_text='Porcentaje de ganancia global para todos los productos (ej: 10 para 10%)', max_digits=5)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Configuración Global',
                'verbose_name_plural': 'Configuración Global',
                'db_table': 'configuracion_global',
                'managed': False,
            },
        ),
    ]

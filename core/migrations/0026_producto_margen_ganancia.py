# Generated migration to add margen_ganancia field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_cliente_distribuidor_distribuidorproducto_repartidor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='margen_ganancia',
            field=models.DecimalField(decimal_places=2, default=10, help_text='Porcentaje de ganancia (ej: 10 para 10%)', max_digits=5),
        ),
    ]

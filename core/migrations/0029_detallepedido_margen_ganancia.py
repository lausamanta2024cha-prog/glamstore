# Generated migration to add margen_ganancia to detallepedido

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_remove_producto_margen_ganancia'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallepedido',
            name='margen_ganancia',
            field=models.DecimalField(
                decimal_places=2, 
                default=10, 
                help_text='Margen de ganancia que se cobró en este pedido', 
                max_digits=5
            ),
        ),
    ]

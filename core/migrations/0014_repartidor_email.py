# Generated migration to add email field to Repartidor

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_detallepedido_options_alter_pedido_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='repartidor',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]

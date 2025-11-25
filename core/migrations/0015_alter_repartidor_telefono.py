# Generated migration to increase telefono field size

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_repartidor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repartidor',
            name='telefono',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

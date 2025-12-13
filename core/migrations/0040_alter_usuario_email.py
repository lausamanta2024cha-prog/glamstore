# Generated migration to fix email column size

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_create_imagenes_tables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.CharField(db_column='email', max_length=255, unique=True),
        ),
    ]

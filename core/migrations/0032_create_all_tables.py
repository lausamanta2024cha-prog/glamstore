from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_skip_model_creation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('idCategoria', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombreCategoria', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='categorias/')),
            ],
            options={
                'db_table': 'categoria',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('idSubcategoria', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombreSubcategoria', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('idCategoria', models.ForeignKey(db_column='idCategoria', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.categoria')),
            ],
            options={
                'db_table': 'subcategoria',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombreProducto', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=0)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('lote', models.CharField(blank=True, help_text='Codigo del lote actual', max_length=100, null=True)),
                ('cantidadDisponible', models.IntegerField(db_column='cantidadDisponible', default=0)),
                ('fechaIngreso', models.DateTimeField(blank=True, db_column='fechaIngreso', null=True)),
                ('fechaVencimiento', models.DateField(blank=True, db_column='fechaVencimiento', null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos/')),
                ('precio_venta', models.DecimalField(decimal_places=2, default=0, help_text='Precio de venta calculado automaticamente', max_digits=10)),
                ('idCategoria', models.ForeignKey(db_column='idCategoria', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.categoria')),
                ('idSubcategoria', models.ForeignKey(db_column='idSubcategoria', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.subcategoria')),
            ],
            options={
                'db_table': 'productos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('idCliente', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombreCliente', models.CharField(max_length=100)),
                ('apellidoCliente', models.CharField(max_length=100)),
                ('emailCliente', models.EmailField(max_length=100, unique=True)),
                ('telefonoCliente', models.CharField(blank=True, max_length=20, null=True)),
                ('direccionCliente', models.TextField(blank=True, null=True)),
                ('ciudadCliente', models.CharField(blank=True, max_length=50, null=True)),
                ('departamentoCliente', models.CharField(blank=True, max_length=50, null=True)),
                ('codigoPostalCliente', models.CharField(blank=True, max_length=20, null=True)),
                ('usuario', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'db_table': 'clientes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('idPedido', models.BigAutoField(primary_key=True, serialize=False)),
                ('fechaPedido', models.DateTimeField(auto_now_add=True, db_column='fechaPedido')),
                ('estado', models.CharField(choices=[('En Preparacion', 'En Preparacion'), ('En Camino', 'En Camino'), ('Entregado', 'Entregado'), ('Completado', 'Completado'), ('Cancelado', 'Cancelado'), ('Confirmado', 'Confirmado'), ('Devuelto', 'Devuelto')], default='En Preparacion', max_length=50)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('idCliente', models.ForeignKey(db_column='idCliente', on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
            ],
            options={
                'db_table': 'pedidos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('idDetallePedido', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precioUnitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('margen_ganancia', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('idPedido', models.ForeignKey(db_column='idPedido', on_delete=django.db.models.deletion.CASCADE, to='core.pedido')),
                ('idProducto', models.ForeignKey(db_column='idProducto', on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
            options={
                'db_table': 'detallepedido',
                'managed': True,
            },
        ),
    ]

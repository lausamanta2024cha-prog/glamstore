#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models.categoria import Categoria, Subcategoria
from core.models.productos import Producto

# Datos reales de categorias (del backup mas reciente)
CATEGORIAS = [
    {'idCategoria': 1, 'nombreCategoria': 'Rostro', 'descripcion': 'Base, correctores, polvos compactos, rubores e iluminadores', 'imagen': 'categorias/rostro.avif'},
    {'idCategoria': 2, 'nombreCategoria': 'Ojos', 'descripcion': 'Sombras, delineadores, pestaninas y cejas', 'imagen': 'categorias/ojos.jpg'},
    {'idCategoria': 3, 'nombreCategoria': 'Labios', 'descripcion': 'Labiales, brillos y delineadores de labios', 'imagen': 'categorias/la.jpg'},
    {'idCategoria': 4, 'nombreCategoria': 'Unas', 'descripcion': 'Esmaltes, tratamientos y accesorios para unas', 'imagen': 'categorias/uñas.webp'},
    {'idCategoria': 5, 'nombreCategoria': 'Accesorios', 'descripcion': 'Brochas, esponjas y herramientas de maquillaje', 'imagen': 'categorias/accessories_feb_main.jpg'},
    {'idCategoria': 9, 'nombreCategoria': 'Cuidado Facial', 'descripcion': 'cremas,serums', 'imagen': 'categorias/cuidado_facial_T4konPk.jpg'},
]

# Datos reales de subcategorias (del backup mas reciente)
SUBCATEGORIAS = [
    {'idSubcategoria': 1, 'nombreSubcategoria': 'Base', 'idCategoria': 1},
    {'idSubcategoria': 2, 'nombreSubcategoria': 'Correctores', 'idCategoria': 1},
    {'idSubcategoria': 3, 'nombreSubcategoria': 'Polvos compactos', 'idCategoria': 1},
    {'idSubcategoria': 4, 'nombreSubcategoria': 'Rubores', 'idCategoria': 1},
    {'idSubcategoria': 5, 'nombreSubcategoria': 'Iluminadores', 'idCategoria': 1},
    {'idSubcategoria': 6, 'nombreSubcategoria': 'Sombras', 'idCategoria': 2},
    {'idSubcategoria': 7, 'nombreSubcategoria': 'Delineadores', 'idCategoria': 2},
    {'idSubcategoria': 8, 'nombreSubcategoria': 'Pestanas', 'idCategoria': 2},
    {'idSubcategoria': 9, 'nombreSubcategoria': 'Cejas', 'idCategoria': 2},
    {'idSubcategoria': 10, 'nombreSubcategoria': 'Labiales', 'idCategoria': 3},
    {'idSubcategoria': 11, 'nombreSubcategoria': 'Brillos', 'idCategoria': 3},
    {'idSubcategoria': 12, 'nombreSubcategoria': 'Balsamos', 'idCategoria': 3},
    {'idSubcategoria': 13, 'nombreSubcategoria': 'Delineadores de labios', 'idCategoria': 3},
    {'idSubcategoria': 14, 'nombreSubcategoria': 'Esmaltes', 'idCategoria': 4},
    {'idSubcategoria': 15, 'nombreSubcategoria': 'Tratamientos', 'idCategoria': 4},
    {'idSubcategoria': 16, 'nombreSubcategoria': 'Decoracion', 'idCategoria': 4},
    {'idSubcategoria': 17, 'nombreSubcategoria': 'Brochas', 'idCategoria': 5},
    {'idSubcategoria': 18, 'nombreSubcategoria': 'Esponjas', 'idCategoria': 5},
    {'idSubcategoria': 19, 'nombreSubcategoria': 'Organizadores', 'idCategoria': 5},
    {'idSubcategoria': 25, 'nombreSubcategoria': 'espejo', 'idCategoria': 1},
    {'idSubcategoria': 27, 'nombreSubcategoria': 'Bronceadores', 'idCategoria': 1},
    {'idSubcategoria': 28, 'nombreSubcategoria': 'Serums', 'idCategoria': 9},
]

# Datos reales de productos (del backup mas reciente)
PRODUCTOS = [
    {'idProducto': 7700000000001, 'nombreProducto': 'Rubor Rosado Glow', 'precio': 34000.00, 'stock': 469, 'descripcion': 'Rubor en polvo con acabado satinado y pigmento suave.', 'lote': 'L2025-11', 'cantidadDisponible': 50, 'fechaIngreso': '2025-11-07 07:01:07', 'fechaVencimiento': '2027-11-01', 'idCategoria': 1, 'imagen': 'productos/rubor.jpg', 'idSubcategoria': 4, 'precio_venta': 44100},
    {'idProducto': 7700000000002, 'nombreProducto': 'Iluminador Perla Glam', 'precio': 32000.00, 'stock': 387, 'descripcion': 'Ilumina tus mejillas con un brillo nacarado y elegante.', 'lote': 'L2025-11', 'cantidadDisponible': 35, 'fechaIngreso': '2025-11-07 07:01:07', 'fechaVencimiento': '2027-11-01', 'idCategoria': 1, 'imagen': 'productos/ilumi_p.webp', 'idSubcategoria': 5, 'precio_venta': 41500},
    {'idProducto': 7700000000003, 'nombreProducto': 'Corrector Liquido Soft Touch', 'precio': 29000.00, 'stock': 615, 'descripcion': 'Cobertura media con textura ligera y acabado natural.', 'lote': 'L2025-11', 'cantidadDisponible': 40, 'fechaIngreso': '2025-11-07 07:01:07', 'fechaVencimiento': '2027-11-01', 'idCategoria': 1, 'imagen': 'productos/corrector.avif', 'idSubcategoria': 2, 'precio_venta': 37600},
    {'idProducto': 7700000000004, 'nombreProducto': 'Polvo Compacto Mate Glam', 'precio': 38000.00, 'stock': 526, 'descripcion': 'Controla el brillo con un acabado mate y aterciopelado.', 'lote': 'L2025-11', 'cantidadDisponible': 45, 'fechaIngreso': '2025-11-07 07:01:07', 'fechaVencimiento': '2027-11-01', 'idCategoria': 1, 'imagen': 'productos/base_polvo.webp', 'idSubcategoria': 3, 'precio_venta': 49300},
    {'idProducto': 7700000000005, 'nombreProducto': 'Base Cushion Glow', 'precio': 58000.00, 'stock': 336, 'descripcion': 'Base ligera con esponja cushion y efecto luminoso.', 'lote': 'L2025-11', 'cantidadDisponible': 30, 'fechaIngreso': '2025-11-07 07:01:07', 'fechaVencimiento': '2027-11-01', 'idCategoria': 1, 'imagen': 'productos/base.png', 'idSubcategoria': 1, 'precio_venta': 75250},
    {'idProducto': 7700000000011, 'nombreProducto': 'Sombra Cuarteto Rosa', 'precio': 42000.00, 'stock': 101, 'descripcion': 'Paleta de 4 tonos rosados con acabado satinado.', 'lote': 'L2025-11', 'cantidadDisponible': 50, 'fechaIngreso': '2025-11-07 07:01:16', 'fechaVencimiento': '2027-11-01', 'idCategoria': 2, 'imagen': 'productos/s.jpg', 'idSubcategoria': 6, 'precio_venta': 54500},
    {'idProducto': 7700000000012, 'nombreProducto': 'Delineador Liquido Precisio', 'precio': 18000.00, 'stock': 99, 'descripcion': 'Punta fina para trazos definidos y resistentes al agua.', 'lote': 'L2025-11', 'cantidadDisponible': 60, 'fechaIngreso': '2025-11-07 07:01:16', 'fechaVencimiento': '2027-11-01', 'idCategoria': 2, 'imagen': 'productos/delini.webp', 'idSubcategoria': 7, 'precio_venta': 23350},
    {'idProducto': 7700000000013, 'nombreProducto': 'Pestanina Curvas Glam', 'precio': 16000.00, 'stock': 45, 'descripcion': 'Define y curva tus pestanas con formula ligera.', 'lote': 'L2025-11', 'cantidadDisponible': 40, 'fechaIngreso': '2025-11-07 07:01:16', 'fechaVencimiento': '2026-11-01', 'idCategoria': 2, 'imagen': 'productos/pestanina.webp', 'idSubcategoria': 8, 'precio_venta': 20750},
    {'idProducto': 7700000000014, 'nombreProducto': 'Gel para Cejas Natural Brow', 'precio': 20000.00, 'stock': 37, 'descripcion': 'Fija y da forma a tus cejas con acabado natural.', 'lote': 'L2025-11', 'cantidadDisponible': 35, 'fechaIngreso': '2025-11-07 07:01:16', 'fechaVencimiento': '2027-11-01', 'idCategoria': 2, 'imagen': 'productos/pinta_cejaz.avif', 'idSubcategoria': 9, 'precio_venta': 25950},
    {'idProducto': 7700000000015, 'nombreProducto': 'Sombra Liquida Glitter Pop', 'precio': 25000.00, 'stock': 45, 'descripcion': 'Brillo liquido para parpados con efecto multidimensional.', 'lote': 'L2025-11', 'cantidadDisponible': 30, 'fechaIngreso': '2025-11-07 07:01:16', 'fechaVencimiento': '2027-11-01', 'idCategoria': 2, 'imagen': 'productos/l.webp', 'idSubcategoria': 6, 'precio_venta': 32450},
    {'idProducto': 7700000000021, 'nombreProducto': 'Brillo Labial Cristal', 'precio': 22000.00, 'stock': 11, 'descripcion': 'Gloss transparente con efecto volumen y aroma a vainilla.', 'lote': 'L2025-11', 'cantidadDisponible': 50, 'fechaIngreso': '2025-11-07 07:01:25', 'fechaVencimiento': '2027-11-01', 'idCategoria': 3, 'imagen': 'productos/ll.webp', 'idSubcategoria': 11, 'precio_venta': 28550},
    {'idProducto': 7700000000023, 'nombreProducto': 'Balsamo Hidratante Berry Kis', 'precio': 18000.00, 'stock': 44, 'descripcion': 'Hidratacion profunda con aroma a frutos rojos.', 'lote': 'L2025-11', 'cantidadDisponible': -60, 'fechaIngreso': '2025-11-07 07:01:25', 'fechaVencimiento': '2027-11-01', 'idCategoria': 3, 'imagen': 'productos/balsamo.webp', 'idSubcategoria': 12, 'precio_venta': 23350},
    {'idProducto': 7700000000024, 'nombreProducto': 'Delineador de Labios Coral Chic', 'precio': 15000.00, 'stock': 117, 'descripcion': 'Define y realza con precision y suavidad.', 'lote': 'L2025-11', 'cantidadDisponible': -14, 'fechaIngreso': '2025-11-07 07:01:25', 'fechaVencimiento': '2027-11-01', 'idCategoria': 3, 'imagen': 'productos/dd.webp', 'idSubcategoria': 13, 'precio_venta': 19450},
    {'idProducto': 7700000000025, 'nombreProducto': 'Labial Cremoso Fucsia Pop', 'precio': 30000.00, 'stock': 13, 'descripcion': 'Color vibrante con textura cremosa y humectante.', 'lote': 'L2025-11', 'cantidadDisponible': 45, 'fechaIngreso': '2025-11-07 07:01:25', 'fechaVencimiento': '2027-11-01', 'idCategoria': 3, 'imagen': 'productos/la.webp', 'idSubcategoria': 10, 'precio_venta': 38900},
    {'idProducto': 7700000000031, 'nombreProducto': 'Esmalte Rosa Pastel', 'precio': 12000.00, 'stock': 11, 'descripcion': 'Color suave, formula vegana y secado rapido.', 'lote': 'L2025-11', 'cantidadDisponible': 50, 'fechaIngreso': '2025-11-07 07:01:33', 'fechaVencimiento': '2027-11-01', 'idCategoria': 4, 'imagen': 'productos/esm.webp', 'idSubcategoria': 14, 'precio_venta': 15550},
    {'idProducto': 7700000000032, 'nombreProducto': 'Top Coat Brillo Extremo', 'precio': 14000.00, 'stock': 5, 'descripcion': 'Proteccion y brillo espejo para tus unas.', 'lote': 'L2025-11', 'cantidadDisponible': 40, 'fechaIngreso': '2025-11-07 07:01:33', 'fechaVencimiento': '2027-11-01', 'idCategoria': 4, 'imagen': 'productos/top.jpg', 'idSubcategoria': 15, 'precio_venta': 18150},
    {'idProducto': 7700000000033, 'nombreProducto': 'Tratamiento Fortalecedor', 'precio': 18000.00, 'stock': 11, 'descripcion': 'Fortalece unas quebradizas con queratina y calcio.', 'lote': 'L2025-11', 'cantidadDisponible': 3, 'fechaIngreso': '2025-11-07 07:01:33', 'fechaVencimiento': '2027-11-01', 'idCategoria': 4, 'imagen': 'productos/tr.webp', 'idSubcategoria': 15, 'precio_venta': 23350},
    {'idProducto': 7700000000034, 'nombreProducto': 'Esmalte Glitter Champagne', 'precio': 15000.00, 'stock': 21, 'descripcion': 'Brillo dorado para un acabado festivo y glamuroso.', 'lote': 'L2025-11', 'cantidadDisponible': 35, 'fechaIngreso': '2025-11-07 07:01:33', 'fechaVencimiento': '2027-11-01', 'idCategoria': 4, 'imagen': 'productos/ess.webp', 'idSubcategoria': 14, 'precio_venta': 19450},
    {'idProducto': 7700000000035, 'nombreProducto': 'Kit Decoracion de Unas', 'precio': 5000.00, 'stock': 101, 'descripcion': 'Piedras, stickers y pinceles para disenos creativos.', 'lote': 'L2025-11', 'cantidadDisponible': 20, 'fechaIngreso': '2025-11-07 07:01:33', 'fechaVencimiento': '2027-11-01', 'idCategoria': 4, 'imagen': 'productos/ki.webp', 'idSubcategoria': 16, 'precio_venta': 6500},
    {'idProducto': 7700000000041, 'nombreProducto': 'Set de Brochas Rosa Gold', 'precio': 48000.00, 'stock': 12, 'descripcion': '10 brochas suaves para rostro y ojos en estuche glam.', 'lote': 'L2025-11', 'cantidadDisponible': 25, 'fechaIngreso': '2025-11-07 07:01:41', 'fechaVencimiento': '2028-01-01', 'idCategoria': 5, 'imagen': 'productos/br.webp', 'idSubcategoria': 17, 'precio_venta': 62250},
    {'idProducto': 7700000000042, 'nombreProducto': 'Esponja Blender Lavanda', 'precio': 15000.00, 'stock': 15, 'descripcion': 'Esponja suave para base y corrector, acabado uniforme.', 'lote': 'L2025-11', 'cantidadDisponible': 40, 'fechaIngreso': '2025-11-07 07:01:41', 'fechaVencimiento': '2028-01-01', 'idCategoria': 5, 'imagen': 'productos/esp.webp', 'idSubcategoria': 18, 'precio_venta': 19450},
    {'idProducto': 7700000000043, 'nombreProducto': 'Pinza de Cejas Glam', 'precio': 12000.00, 'stock': 16, 'descripcion': 'Precision y diseno ergonomico en acabado metalico rosado.', 'lote': 'L2025-11', 'cantidadDisponible': 50, 'fechaIngreso': '2025-11-07 07:01:41', 'fechaVencimiento': '2028-01-01', 'idCategoria': 5, 'imagen': 'productos/pinzas.webp', 'idSubcategoria': 9, 'precio_venta': 15550},
    {'idProducto': 7700000000044, 'nombreProducto': 'Organizador Acrilico Mini', 'precio': 28000.00, 'stock': 14, 'descripcion': 'Guarda tus productos con estilo y orden.', 'lote': 'L2025-11', 'cantidadDisponible': 30, 'fechaIngreso': '2025-11-07 07:01:41', 'fechaVencimiento': '2028-01-01', 'idCategoria': 5, 'imagen': 'productos/o.webp', 'idSubcategoria': 19, 'precio_venta': 36300},
    {'idProducto': 7700000000045, 'nombreProducto': 'Espejo LED Glam', 'precio': 35000.00, 'stock': 55, 'descripcion': 'Espejo compacto con luz LED y aumento x5.', 'lote': 'L2025-11', 'cantidadDisponible': 20, 'fechaIngreso': '2025-11-07 07:01:41', 'fechaVencimiento': '2028-01-01', 'idCategoria': 5, 'imagen': 'productos/es.jpg', 'idSubcategoria': 19, 'precio_venta': 45400},
    {'idProducto': 7701122334455, 'nombreProducto': 'Labial Mate Velvet Glam', 'precio': 5000.00, 'stock': 84, 'descripcion': 'Color intenso, textura aterciopelada, larga duracion', 'lote': 'L2025-11', 'cantidadDisponible': 40, 'fechaIngreso': '2025-11-05 15:45:00', 'fechaVencimiento': '2027-05-05', 'idCategoria': 3, 'imagen': 'productos/red_velved.jpg', 'idSubcategoria': 10, 'precio_venta': 6500},
    {'idProducto': 7701234567890, 'nombreProducto': 'Base Liquida HD Glam', 'precio': 55000.00, 'stock': 198, 'descripcion': 'Cobertura alta, acabado natural, ideal para piel mixta', 'lote': 'L2025-10', 'cantidadDisponible': 25, 'fechaIngreso': '2025-11-05 15:45:00', 'fechaVencimiento': '2027-11-05', 'idCategoria': 1, 'imagen': 'productos/otra_b.webp', 'idSubcategoria': 1, 'precio_venta': 71350},
    {'idProducto': 7709876543210, 'nombreProducto': 'Pestanina Volumen Total Gla', 'precio': 15000.00, 'stock': 15, 'descripcion': 'Volumen extremo, resistente al agua, formula vegana', 'lote': 'L2025-11', 'cantidadDisponible': 30, 'fechaIngreso': '2025-11-05 15:45:00', 'fechaVencimiento': '2026-11-05', 'idCategoria': 2, 'imagen': 'productos/p.webp', 'idSubcategoria': 8, 'precio_venta': 19450},
    {'idProducto': 7709876543220, 'nombreProducto': 'Bronceador trendy', 'precio': 15000.00, 'stock': 16, 'descripcion': 'Bronceador de trendy', 'lote': None, 'cantidadDisponible': -10, 'fechaIngreso': '2025-11-26 16:24:35', 'fechaVencimiento': None, 'idCategoria': 1, 'imagen': 'productos/bronceador.jpg', 'idSubcategoria': 27, 'precio_venta': 19450},
    {'idProducto': 7709876543221, 'nombreProducto': 'Serum Centella Asiática', 'precio': 8500.00, 'stock': 8, 'descripcion': 'Serum Centella Asiática Antiedad Calmante Control Poros Tipo De Piel Todo Tipo', 'lote': None, 'cantidadDisponible': 0, 'fechaIngreso': '2025-12-10 19:03:58', 'fechaVencimiento': None, 'idCategoria': 9, 'imagen': 'productos/Serum_Centella_Asiática_Antiedad_Calmante_Control_Poros_Tipo_De_Piel_Todo_Tipo_h3J3iRp.png', 'idSubcategoria': 28, 'precio_venta': 11050},
]

try:
    # Insertar categorias
    for cat_data in CATEGORIAS:
        cat, created = Categoria.objects.get_or_create(
            idCategoria=cat_data['idCategoria'],
            defaults={
                'nombreCategoria': cat_data['nombreCategoria'],
                'descripcion': cat_data['descripcion'],
                'imagen': cat_data['imagen'],
            }
        )
        if created:
            print(f"Categoría creada: {cat.nombreCategoria}")
    
    # Insertar subcategorias
    for subcat_data in SUBCATEGORIAS:
        try:
            categoria = Categoria.objects.get(idCategoria=subcat_data['idCategoria'])
            subcat, created = Subcategoria.objects.get_or_create(
                idSubcategoria=subcat_data['idSubcategoria'],
                defaults={
                    'nombreSubcategoria': subcat_data['nombreSubcategoria'],
                    'idCategoria': categoria,
                }
            )
            if created:
                print(f"Subcategoría creada: {subcat.nombreSubcategoria}")
        except Categoria.DoesNotExist:
            print(f"Categoría {subcat_data['idCategoria']} no encontrada para subcategoría {subcat_data['idSubcategoria']}")
    
    # Insertar productos
    for prod_data in PRODUCTOS:
        try:
            categoria = Categoria.objects.get(idCategoria=prod_data['idCategoria'])
            subcategoria = None
            if prod_data['idSubcategoria']:
                subcategoria = Subcategoria.objects.get(idSubcategoria=prod_data['idSubcategoria'])
            
            prod, created = Producto.objects.get_or_create(
                idProducto=prod_data['idProducto'],
                defaults={
                    'nombreProducto': prod_data['nombreProducto'],
                    'precio': prod_data['precio'],
                    'stock': prod_data['stock'],
                    'descripcion': prod_data['descripcion'],
                    'lote': prod_data['lote'],
                    'cantidadDisponible': prod_data['cantidadDisponible'],
                    'fechaIngreso': prod_data['fechaIngreso'],
                    'fechaVencimiento': prod_data['fechaVencimiento'],
                    'idCategoria': categoria,
                    'imagen': prod_data['imagen'],
                    'idSubcategoria': subcategoria,
                    'precio_venta': prod_data['precio_venta'],
                }
            )
            if created:
                print(f"Producto creado: {prod.nombreProducto}")
        except (Categoria.DoesNotExist, Subcategoria.DoesNotExist) as e:
            print(f"Error al crear producto {prod_data['idProducto']}: {e}")
    
    print("\nDatos de categorías, subcategorías y productos restaurados exitosamente")
except Exception as e:
    print(f"Error al restaurar datos: {e}")
    import traceback
    traceback.print_exc()

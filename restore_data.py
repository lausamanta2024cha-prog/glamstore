#!/usr/bin/env python
import os
import django
from django.conf import settings
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

# Datos reales de categorias (del backup mas reciente)
CATEGORIAS = [
    (1, 'Rostro', 'Base, correctores, polvos compactos, rubores e iluminadores', 'categorias/rostro.avif'),
    (2, 'Ojos', 'Sombras, delineadores, pestaninas y cejas', 'categorias/ojos.jpg'),
    (3, 'Labios', 'Labiales, brillos y delineadores de labios', 'categorias/la.jpg'),
    (4, 'Unas', 'Esmaltes, tratamientos y accesorios para unas', 'categorias/uñas.webp'),
    (5, 'Accesorios', 'Brochas, esponjas y herramientas de maquillaje', 'categorias/accessories_feb_main.jpg'),
    (9, 'Cuidado Facial', 'cremas,serums', 'categorias/cuidado_facial_T4konPk.jpg'),
]

# Datos reales de subcategorias (del backup mas reciente)
SUBCATEGORIAS = [
    (1, 'Base', 1),
    (2, 'Correctores', 1),
    (3, 'Polvos compactos', 1),
    (4, 'Rubores', 1),
    (5, 'Iluminadores', 1),
    (6, 'Sombras', 2),
    (7, 'Delineadores', 2),
    (8, 'Pestanas', 2),
    (9, 'Cejas', 2),
    (10, 'Labiales', 3),
    (11, 'Brillos', 3),
    (12, 'Balsamos', 3),
    (13, 'Delineadores de labios', 3),
    (14, 'Esmaltes', 4),
    (15, 'Tratamientos', 4),
    (16, 'Decoracion', 4),
    (17, 'Brochas', 5),
    (18, 'Esponjas', 5),
    (19, 'Organizadores', 5),
    (25, 'espejo', 1),
    (27, 'Bronceadores', 1),
    (28, 'Serums', 9),
]

# Datos reales de productos (del backup mas reciente)
PRODUCTOS = [
    (7700000000001, 'Rubor Rosado Glow', 34000.00, 469, 'Rubor en polvo con acabado satinado y pigmento suave.', 'L2025-11', 50, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/rubor.jpg', 4, 44100),
    (7700000000002, 'Iluminador Perla Glam', 32000.00, 387, 'Ilumina tus mejillas con un brillo nacarado y elegante.', 'L2025-11', 35, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/ilumi_p.webp', 5, 41500),
    (7700000000003, 'Corrector Liquido Soft Touch', 29000.00, 615, 'Cobertura media con textura ligera y acabado natural.', 'L2025-11', 40, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/corrector.avif', 2, 37600),
    (7700000000004, 'Polvo Compacto Mate Glam', 38000.00, 526, 'Controla el brillo con un acabado mate y aterciopelado.', 'L2025-11', 45, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/base_polvo.webp', 3, 49300),
    (7700000000005, 'Base Cushion Glow', 58000.00, 336, 'Base ligera con esponja cushion y efecto luminoso.', 'L2025-11', 30, '2025-11-07 07:01:07', '2027-11-01', 1, 'productos/base.png', 1, 75250),
    (7700000000011, 'Sombra Cuarteto Rosa', 42000.00, 101, 'Paleta de 4 tonos rosados con acabado satinado.', 'L2025-11', 50, '2025-11-07 07:01:16', '2027-11-01', 2, 'productos/s.jpg', 6, 54500),
    (7700000000012, 'Delineador Liquido Precisio', 18000.00, 99, 'Punta fina para trazos definidos y resistentes al agua.', 'L2025-11', 60, '2025-11-07 07:01:16', '2027-11-01', 2, 'productos/delini.webp', 7, 23350),
    (7700000000013, 'Pestanina Curvas Glam', 16000.00, 45, 'Define y curva tus pestanas con formula ligera.', 'L2025-11', 40, '2025-11-07 07:01:16', '2026-11-01', 2, 'productos/pestanina.webp', 8, 20750),
    (7700000000014, 'Gel para Cejas Natural Brow', 20000.00, 37, 'Fija y da forma a tus cejas con acabado natural.', 'L2025-11', 35, '2025-11-07 07:01:16', '2027-11-01', 2, 'productos/pinta_cejaz.avif', 9, 25950),
    (7700000000015, 'Sombra Liquida Glitter Pop', 25000.00, 45, 'Brillo liquido para parpados con efecto multidimensional.', 'L2025-11', 30, '2025-11-07 07:01:16', '2027-11-01', 2, 'productos/l.webp', 6, 32450),
    (7700000000021, 'Brillo Labial Cristal', 22000.00, 11, 'Gloss transparente con efecto volumen y aroma a vainilla.', 'L2025-11', 50, '2025-11-07 07:01:25', '2027-11-01', 3, 'productos/ll.webp', 11, 28550),
    (7700000000023, 'Balsamo Hidratante Berry Kis', 18000.00, 44, 'Hidratacion profunda con aroma a frutos rojos.', 'L2025-11', -60, '2025-11-07 07:01:25', '2027-11-01', 3, 'productos/balsamo.webp', 12, 23350),
    (7700000000024, 'Delineador de Labios Coral Chic', 15000.00, 117, 'Define y realza con precision y suavidad.', 'L2025-11', -14, '2025-11-07 07:01:25', '2027-11-01', 3, 'productos/dd.webp', 13, 19450),
    (7700000000025, 'Labial Cremoso Fucsia Pop', 30000.00, 13, 'Color vibrante con textura cremosa y humectante.', 'L2025-11', 45, '2025-11-07 07:01:25', '2027-11-01', 3, 'productos/la.webp', 10, 38900),
    (7700000000031, 'Esmalte Rosa Pastel', 12000.00, 11, 'Color suave, formula vegana y secado rapido.', 'L2025-11', 50, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/esm.webp', 14, 15550),
    (7700000000032, 'Top Coat Brillo Extremo', 14000.00, 5, 'Proteccion y brillo espejo para tus unas.', 'L2025-11', 40, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/top.jpg', 15, 18150),
    (7700000000033, 'Tratamiento Fortalecedor', 18000.00, 11, 'Fortalece unas quebradizas con queratina y calcio.', 'L2025-11', 3, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/tr.webp', 15, 23350),
    (7700000000034, 'Esmalte Glitter Champagne', 15000.00, 21, 'Brillo dorado para un acabado festivo y glamuroso.', 'L2025-11', 35, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/ess.webp', 14, 19450),
    (7700000000035, 'Kit Decoracion de Unas', 5000.00, 101, 'Piedras, stickers y pinceles para disenos creativos.', 'L2025-11', 20, '2025-11-07 07:01:33', '2027-11-01', 4, 'productos/ki.webp', 16, 6500),
    (7700000000041, 'Set de Brochas Rosa Gold', 48000.00, 12, '10 brochas suaves para rostro y ojos en estuche glam.', 'L2025-11', 25, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/br.webp', 17, 62250),
    (7700000000042, 'Esponja Blender Lavanda', 15000.00, 15, 'Esponja suave para base y corrector, acabado uniforme.', 'L2025-11', 40, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/esp.webp', 18, 19450),
    (7700000000043, 'Pinza de Cejas Glam', 12000.00, 16, 'Precision y diseno ergonomico en acabado metalico rosado.', 'L2025-11', 50, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/pinzas.webp', 9, 15550),
    (7700000000044, 'Organizador Acrilico Mini', 28000.00, 14, 'Guarda tus productos con estilo y orden.', 'L2025-11', 30, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/o.webp', 19, 36300),
    (7700000000045, 'Espejo LED Glam', 35000.00, 55, 'Espejo compacto con luz LED y aumento x5.', 'L2025-11', 20, '2025-11-07 07:01:41', '2028-01-01', 5, 'productos/es.jpg', 19, 45400),
    (7701122334455, 'Labial Mate Velvet Glam', 5000.00, 84, 'Color intenso, textura aterciopelada, larga duracion', 'L2025-11', 40, '2025-11-05 15:45:00', '2027-05-05', 3, 'productos/red_velved.jpg', 10, 6500),
    (7701234567890, 'Base Liquida HD Glam', 55000.00, 198, 'Cobertura alta, acabado natural, ideal para piel mixta', 'L2025-10', 25, '2025-11-05 15:45:00', '2027-11-05', 1, 'productos/otra_b.webp', 1, 71350),
    (7709876543210, 'Pestanina Volumen Total Gla', 15000.00, 15, 'Volumen extremo, resistente al agua, formula vegana', 'L2025-11', 30, '2025-11-05 15:45:00', '2026-11-05', 2, 'productos/p.webp', 8, 19450),
    (7709876543220, 'Bronceador trendy', 15000.00, 16, 'Bronceador de trendy', None, -10, '2025-11-26 16:24:35', None, 1, 'productos/bronceador.jpg', 27, 19450),
    (7709876543221, 'Serum Centella Asiática', 8500.00, 8, 'Serum Centella Asiática Antiedad Calmante Control Poros Tipo De Piel Todo Tipo', None, 0, '2025-12-10 19:03:58', None, 9, 'productos/Serum_Centella_Asiática_Antiedad_Calmante_Control_Poros_Tipo_De_Piel_Todo_Tipo_h3J3iRp.png', 28, 11050),
]

try:
    with connection.cursor() as cursor:
        # Insertar categorias
        for cat in CATEGORIAS:
            cursor.execute(
                'INSERT OR IGNORE INTO categorias (idCategoria, nombreCategoria, descripcion, imagen) VALUES (?, ?, ?, ?)',
                cat
            )
        
        # Insertar subcategorias
        for subcat in SUBCATEGORIAS:
            cursor.execute(
                'INSERT OR IGNORE INTO subcategorias (idSubcategoria, nombreSubcategoria, idCategoria) VALUES (?, ?, ?)',
                subcat
            )
        
        # Insertar productos
        for prod in PRODUCTOS:
            cursor.execute(
                '''INSERT OR IGNORE INTO productos 
                (idProducto, nombreProducto, precio, stock, descripcion, lote, cantidadDisponible, 
                fechaIngreso, fechaVencimiento, idCategoria, imagen, idSubcategoria, precio_venta) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                prod
            )
    
    print("Datos restaurados exitosamente")
except Exception as e:
    print(f"Error al restaurar datos: {e}")

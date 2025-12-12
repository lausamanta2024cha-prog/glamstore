#!/usr/bin/env python
import os
import django
from django.conf import settings
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

print("Restaurando categorias, subcategorias y productos...")
from core.models.categoria import Categoria, Subcategoria
from core.models.productos import Producto

CATEGORIAS = [
    {'idCategoria': 1, 'nombreCategoria': 'Rostro', 'descripcion': 'Base, correctores, polvos compactos, rubores e iluminadores', 'imagen': 'categorias/rostro.avif'},
    {'idCategoria': 2, 'nombreCategoria': 'Ojos', 'descripcion': 'Sombras, delineadores, pestaninas y cejas', 'imagen': 'categorias/ojos.jpg'},
    {'idCategoria': 3, 'nombreCategoria': 'Labios', 'descripcion': 'Labiales, brillos y delineadores de labios', 'imagen': 'categorias/la.jpg'},
    {'idCategoria': 4, 'nombreCategoria': 'Unas', 'descripcion': 'Esmaltes, tratamientos y accesorios para unas', 'imagen': 'categorias/uñas.webp'},
    {'idCategoria': 5, 'nombreCategoria': 'Accesorios', 'descripcion': 'Brochas, esponjas y herramientas de maquillaje', 'imagen': 'categorias/accessories_feb_main.jpg'},
    {'idCategoria': 9, 'nombreCategoria': 'Cuidado Facial', 'descripcion': 'cremas,serums', 'imagen': 'categorias/cuidado_facial_T4konPk.jpg'},
]

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
        print(f"  [OK] Categoria: {cat.nombreCategoria}")

print("\n[OK] Restauracion completada exitosamente")

#!/usr/bin/env python
import os
import django
from django.conf import settings
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

print("Restaurando datos de la base de datos...")

# Ahora crear usuarios y datos
print("\nCreando usuarios y datos...")
from core.models import Usuario
from datetime import datetime

USUARIOS = [
    {
        'idUsuario': 10,
        'email': 'glamstore0303777@gmail.com',
        'password': 'pbkdf2_sha256$600000$PpT7bTOmCUOctDntYMUC5K$iLQW1DP7WSCXJQpyNInqAt56x5nvhbHoZD8fGC2kSv8=',
        'id_rol': 1,
        'nombre': 'Glamstore Admin',
        'telefono': '3000000000',
        'direccion': 'Calle Glam 123',
        'fechaCreacion': datetime(2025, 11, 11, 5, 42, 6)
    },
    {
        'idUsuario': 21,
        'email': 'admin123@glamstore.com',
        'password': 'pbkdf2_sha256$600000$H6vyXqLqUoINBizXnvyy0c$a0I72ZuNVaMkLAqYPysxkr+IVE7kercJAzzECxFChYs=',
        'id_rol': 1,
        'nombre': 'Lauren Samanta Ortiz',
        'telefono': None,
        'direccion': None,
        'fechaCreacion': datetime(2025, 11, 24, 13, 40, 20)
    },
]

for user_data in USUARIOS:
    usuario, created = Usuario.objects.get_or_create(
        idUsuario=user_data['idUsuario'],
        defaults={
            'email': user_data['email'],
            'password': user_data['password'],
            'id_rol': user_data['id_rol'],
            'nombre': user_data['nombre'],
            'telefono': user_data['telefono'],
            'direccion': user_data['direccion'],
            'fechaCreacion': user_data['fechaCreacion'],
        }
    )
    if created:
        print(f"  [OK] Usuario creado: {usuario.nombre}")
    else:
        print(f"  [OK] Usuario ya existe: {usuario.nombre}")

print("\n[OK] Inicializacion completada exitosamente")

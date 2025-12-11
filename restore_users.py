#!/usr/bin/env python
import os
import django
from django.contrib.auth.hashers import make_password
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from core.models import Usuario

# Datos de usuarios con roles
USUARIOS = [
    {
        'idUsuario': 10,
        'email': 'glamstore0303777@gmail.com',
        'password': 'pbkdf2_sha256$600000$PpT7bTOmCUOctDntYMUC5K$iLQW1DP7WSCXJQpyNInqAt56x5nvhbHoZD8fGC2kSv8=',
        'id_rol': 1,  # Admin
        'nombre': 'Glamstore Admin',
        'telefono': '3000000000',
        'direccion': 'Calle Glam 123',
        'fechaCreacion': '2025-11-11 05:42:06'
    },
    {
        'idUsuario': 21,
        'email': 'admin123@glamstore.com',
        'password': 'pbkdf2_sha256$600000$H6vyXqLqUoINBizXnvyy0c$a0I72ZuNVaMkLAqYPysxkr+IVE7kercJAzzECxFChYs=',
        'id_rol': 1,  # Admin
        'nombre': 'Lauren Samanta Ortiz',
        'telefono': None,
        'direccion': None,
        'fechaCreacion': '2025-11-24 13:40:20'
    },
]

try:
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
            print(f"✓ Usuario creado: {usuario.nombre} (Rol: {usuario.id_rol})")
        else:
            print(f"✓ Usuario ya existe: {usuario.nombre} (Rol: {usuario.id_rol})")
    
    print("\nUsuarios restaurados exitosamente")
    
    # Verificar usuarios
    print("\nUsuarios en la base de datos:")
    for u in Usuario.objects.all():
        print(f"  • {u.nombre} ({u.email}) - Rol: {u.id_rol}")
        
except Exception as e:
    print(f"Error al restaurar usuarios: {e}")
    import traceback
    traceback.print_exc()

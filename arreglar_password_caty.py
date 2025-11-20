"""
Script para arreglar el password del usuario 'caty'
Ejecutar con: python manage.py shell

IMPORTANTE: Edita este script con el email y contraseña correctos antes de ejecutar
"""

from core.models import Usuario
from django.contrib.auth.hashers import make_password

# ⚠️ EDITA ESTOS VALORES CON LOS DATOS CORRECTOS
EMAIL_USUARIO = "caty@gmail.com"  # Cambia esto por el email correcto
NUEVA_PASSWORD = "123456"  # Cambia esto por la contraseña que quieres establecer

print("\n" + "="*60)
print("ARREGLANDO PASSWORD DEL USUARIO")
print("="*60)

try:
    # Buscar el usuario
    usuario = Usuario.objects.get(email=EMAIL_USUARIO)
    
    print(f"\n✅ Usuario encontrado:")
    print(f"   ID: {usuario.idUsuario}")
    print(f"   Nombre: {usuario.nombre}")
    print(f"   Email: {usuario.email}")
    print(f"   Password actual: {usuario.password[:50] if usuario.password else 'NULL'}...")
    
    # Verificar si el password está hasheado
    if usuario.password and (usuario.password.startswith('pbkdf2_sha256$') or usuario.password.startswith('bcrypt$')):
        print(f"\n⚠️  El password ya está hasheado correctamente")
        print(f"   Si no puedes iniciar sesión, el problema puede ser:")
        print(f"   1. La contraseña es incorrecta")
        print(f"   2. El email es incorrecto")
        respuesta = input("\n¿Quieres establecer una nueva contraseña de todos modos? (si/no): ")
        if respuesta.lower() != 'si':
            print("Operación cancelada")
            exit()
    
    # Hashear y guardar la nueva contraseña
    usuario.password = make_password(NUEVA_PASSWORD)
    usuario.save()
    
    print(f"\n✅ Password actualizado exitosamente!")
    print(f"   Nuevo password hash: {usuario.password[:50]}...")
    print(f"\n🎉 Ahora puedes iniciar sesión con:")
    print(f"   Email: {EMAIL_USUARIO}")
    print(f"   Password: {NUEVA_PASSWORD}")
    
except Usuario.DoesNotExist:
    print(f"\n❌ ERROR: No se encontró usuario con email '{EMAIL_USUARIO}'")
    print(f"\nUsuarios disponibles:")
    for u in Usuario.objects.all():
        print(f"   - {u.email} ({u.nombre})")
    print(f"\nEdita el script 'arreglar_password_caty.py' con el email correcto")

except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "="*60)
print("FIN")
print("="*60 + "\n")

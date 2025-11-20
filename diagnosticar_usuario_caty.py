"""
Script de diagnóstico para el usuario 'caty'
Ejecutar con: python manage.py shell < diagnosticar_usuario_caty.py
"""

from core.models import Cliente, Usuario
from django.contrib.auth.hashers import check_password, make_password

print("\n" + "="*60)
print("DIAGNÓSTICO DEL USUARIO 'CATY'")
print("="*60)

# Buscar por nombre 'caty'
print("\n1. BÚSQUEDA POR NOMBRE 'caty':")
usuarios_por_nombre = Usuario.objects.filter(nombre__icontains='caty')
if usuarios_por_nombre.exists():
    for usuario in usuarios_por_nombre:
        print(f"\n   ✅ Usuario encontrado:")
        print(f"      ID: {usuario.idUsuario}")
        print(f"      Nombre: {usuario.nombre}")
        print(f"      Email: {usuario.email}")
        print(f"      Rol: {usuario.id_rol} (1=Admin, 2=Cliente)")
        print(f"      ID Cliente: {usuario.idCliente}")
        print(f"      Password hash: {usuario.password[:50]}...")
        
        # Verificar si el password está hasheado correctamente
        if usuario.password:
            if usuario.password.startswith('pbkdf2_sha256$') or usuario.password.startswith('bcrypt$'):
                print(f"      ✅ Password está hasheado correctamente")
            else:
                print(f"      ⚠️  WARNING: Password NO está hasheado (texto plano)")
                print(f"      Esto causará que el login falle")
        else:
            print(f"      ❌ Password es NULL")
else:
    print("   ❌ No se encontró usuario con nombre 'caty'")

# Buscar por email que contenga 'caty'
print("\n2. BÚSQUEDA POR EMAIL CON 'caty':")
usuarios_por_email = Usuario.objects.filter(email__icontains='caty')
if usuarios_por_email.exists():
    for usuario in usuarios_por_email:
        print(f"\n   ✅ Usuario encontrado:")
        print(f"      ID: {usuario.idUsuario}")
        print(f"      Email: {usuario.email}")
        print(f"      Nombre: {usuario.nombre}")
else:
    print("   ❌ No se encontró usuario con email que contenga 'caty'")

# Buscar cliente con nombre 'caty'
print("\n3. BÚSQUEDA DE CLIENTE CON NOMBRE 'caty':")
clientes = Cliente.objects.filter(nombre__icontains='caty')
if clientes.exists():
    for cliente in clientes:
        print(f"\n   ✅ Cliente encontrado:")
        print(f"      ID: {cliente.idCliente}")
        print(f"      Nombre: {cliente.nombre}")
        print(f"      Email: {cliente.email}")
        
        # Verificar si tiene usuario asociado
        usuario_asociado = Usuario.objects.filter(idCliente=cliente.idCliente).first()
        if usuario_asociado:
            print(f"      ✅ Tiene usuario asociado: ID {usuario_asociado.idUsuario}")
        else:
            print(f"      ⚠️  NO tiene usuario asociado (es cliente invitado)")
else:
    print("   ❌ No se encontró cliente con nombre 'caty'")

# Listar todos los usuarios para referencia
print("\n4. TODOS LOS USUARIOS EN LA BASE DE DATOS:")
todos_usuarios = Usuario.objects.all()
if todos_usuarios.exists():
    for usuario in todos_usuarios:
        print(f"   - ID: {usuario.idUsuario}, Email: {usuario.email}, Nombre: {usuario.nombre}")
else:
    print("   ❌ No hay usuarios en la base de datos")

print("\n" + "="*60)
print("FIN DEL DIAGNÓSTICO")
print("="*60)

# Instrucciones para arreglar el problema
print("\n📋 POSIBLES SOLUCIONES:")
print("\n1. Si el password NO está hasheado:")
print("   from core.models import Usuario")
print("   from django.contrib.auth.hashers import make_password")
print("   usuario = Usuario.objects.get(email='email_de_caty')")
print("   usuario.password = make_password('contraseña_correcta')")
print("   usuario.save()")
print("\n2. Si el usuario no existe:")
print("   Crear el usuario desde /registro/")
print("\n3. Si el email es incorrecto:")
print("   Verificar el email exacto en la base de datos")
print("\n")

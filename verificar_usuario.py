"""
Script de diagnóstico para verificar el estado de usuarios y clientes
Ejecutar con: python manage.py shell < verificar_usuario.py
"""

from core.models import Cliente, Usuario

# Email del usuario a verificar
email = "carlos@gmail.com"

print("\n" + "="*60)
print("DIAGNÓSTICO DE USUARIO")
print("="*60)

# Buscar cliente
try:
    cliente = Cliente.objects.get(email=email)
    print(f"\n✅ CLIENTE ENCONTRADO:")
    print(f"   ID: {cliente.idCliente}")
    print(f"   Nombre: {cliente.nombre}")
    print(f"   Email: {cliente.email}")
    print(f"   Teléfono: {cliente.telefono}")
    print(f"   Dirección: {cliente.direccion}")
except Cliente.DoesNotExist:
    print(f"\n❌ No se encontró cliente con email: {email}")
    cliente = None

# Buscar usuario
if cliente:
    try:
        usuario = Usuario.objects.get(idCliente=cliente.idCliente)
        print(f"\n✅ USUARIO ENCONTRADO:")
        print(f"   ID Usuario: {usuario.idUsuario}")
        print(f"   Email: {usuario.email}")
        print(f"   Nombre: {usuario.nombre}")
        print(f"   Rol: {usuario.id_rol} (1=Admin, 2=Cliente)")
        print(f"   ID Cliente vinculado: {usuario.idCliente}")
        print(f"\n🎯 ESTADO: Usuario Registrado (tiene contraseña)")
        print(f"   ✅ NO debe ver formulario 'Crea tu cuenta ahora'")
    except Usuario.DoesNotExist:
        print(f"\n⚠️  NO SE ENCONTRÓ USUARIO ASOCIADO")
        print(f"   El cliente existe pero no tiene usuario (contraseña)")
        print(f"\n🎯 ESTADO: Cliente Invitado")
        print(f"   ✅ DEBE ver formulario 'Crea tu cuenta ahora'")

# Buscar por email en usuarios directamente
print(f"\n" + "-"*60)
print("BÚSQUEDA ALTERNATIVA POR EMAIL EN USUARIOS:")
print("-"*60)
try:
    usuario_por_email = Usuario.objects.get(email=email)
    print(f"✅ Usuario encontrado por email:")
    print(f"   ID Usuario: {usuario_por_email.idUsuario}")
    print(f"   ID Cliente: {usuario_por_email.idCliente}")
    print(f"   Nombre: {usuario_por_email.nombre}")
    
    if usuario_por_email.idCliente != cliente.idCliente if cliente else None:
        print(f"\n⚠️  ADVERTENCIA: El idCliente del usuario ({usuario_por_email.idCliente})")
        print(f"   no coincide con el idCliente encontrado ({cliente.idCliente if cliente else 'N/A'})")
except Usuario.DoesNotExist:
    print(f"❌ No se encontró usuario con email: {email}")

print("\n" + "="*60)
print("FIN DEL DIAGNÓSTICO")
print("="*60 + "\n")

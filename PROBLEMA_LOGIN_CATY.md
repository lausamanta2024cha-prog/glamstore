# 🔍 Diagnóstico: Problema de Login con Usuario 'caty'

## 🎯 Problema

El usuario 'caty' no puede iniciar sesión en el sistema.

## 🔎 Posibles Causas

### 1. Password en Texto Plano (Más Común)
Si el password se guardó directamente en la base de datos sin hashear, el login fallará porque Django intenta comparar el hash con texto plano.

**Síntoma:**
- El usuario existe en la BD
- El email es correcto
- La contraseña es correcta
- Pero el login falla

**Causa:**
```sql
-- En la base de datos:
password = "123456"  ❌ Texto plano

-- Debería ser:
password = "pbkdf2_sha256$..."  ✅ Hasheado
```

### 2. Email Incorrecto
El usuario intenta iniciar sesión con un email diferente al registrado.

**Ejemplos:**
- Registrado: `caty@gmail.com`
- Intenta con: `caty@hotmail.com` ❌

### 3. Usuario No Existe
El usuario 'caty' no está en la tabla `usuarios`, solo en `clientes`.

### 4. Password NULL
El campo password está vacío en la base de datos.

## 🧪 Diagnóstico

### Paso 1: Ejecutar Script de Diagnóstico

```bash
python manage.py shell < diagnosticar_usuario_caty.py
```

Este script te mostrará:
- ✅ Si el usuario existe
- ✅ Cuál es su email exacto
- ✅ Si el password está hasheado correctamente
- ✅ Si tiene cliente asociado

**Ejemplo de salida:**

```
============================================================
DIAGNÓSTICO DEL USUARIO 'CATY'
============================================================

1. BÚSQUEDA POR NOMBRE 'caty':

   ✅ Usuario encontrado:
      ID: 5
      Nombre: caty
      Email: caty@gmail.com
      Rol: 2 (1=Admin, 2=Cliente)
      ID Cliente: 10
      Password hash: 123456
      ⚠️  WARNING: Password NO está hasheado (texto plano)
      Esto causará que el login falle
```

### Paso 2: Identificar el Problema

Según la salida del diagnóstico:

**Si dice "Password NO está hasheado":**
→ Ir a Solución 1

**Si dice "No se encontró usuario":**
→ Ir a Solución 2

**Si dice "Password es NULL":**
→ Ir a Solución 3

**Si dice "Password está hasheado correctamente":**
→ Ir a Solución 4

## ✅ Soluciones

### Solución 1: Arreglar Password en Texto Plano

**Opción A: Usar el script automático**

1. Editar `arreglar_password_caty.py`:
```python
EMAIL_USUARIO = "caty@gmail.com"  # Email correcto
NUEVA_PASSWORD = "123456"  # Contraseña que quieres establecer
```

2. Ejecutar:
```bash
python manage.py shell < arreglar_password_caty.py
```

**Opción B: Manualmente en Django Shell**

```bash
python manage.py shell
```

```python
from core.models import Usuario
from django.contrib.auth.hashers import make_password

# Buscar el usuario
usuario = Usuario.objects.get(email="caty@gmail.com")

# Establecer nueva contraseña hasheada
usuario.password = make_password("123456")
usuario.save()

print("✅ Password actualizado!")
```

### Solución 2: Crear el Usuario

Si el usuario no existe, crearlo:

```bash
python manage.py shell
```

```python
from core.models import Usuario, Cliente
from django.contrib.auth.hashers import make_password

# Buscar o crear el cliente
cliente, created = Cliente.objects.get_or_create(
    email="caty@gmail.com",
    defaults={
        'nombre': 'Caty',
        'cedula': '123456789',
        'telefono': '3001234567',
        'direccion': 'Calle 123'
    }
)

# Crear el usuario
usuario = Usuario.objects.create(
    nombre='Caty',
    email='caty@gmail.com',
    password=make_password('123456'),  # Contraseña hasheada
    id_rol=2,  # Rol de Cliente
    idCliente=cliente.idCliente
)

print(f"✅ Usuario creado: ID {usuario.idUsuario}")
```

### Solución 3: Establecer Password NULL

```bash
python manage.py shell
```

```python
from core.models import Usuario
from django.contrib.auth.hashers import make_password

usuario = Usuario.objects.get(email="caty@gmail.com")
usuario.password = make_password("123456")
usuario.save()

print("✅ Password establecido!")
```

### Solución 4: Verificar Email y Contraseña

Si el password está hasheado correctamente, el problema es:

1. **Email incorrecto:** Verifica el email exacto en el diagnóstico
2. **Contraseña incorrecta:** Establece una nueva contraseña conocida

```python
from core.models import Usuario
from django.contrib.auth.hashers import make_password

usuario = Usuario.objects.get(email="caty@gmail.com")
usuario.password = make_password("nueva_contraseña_123")
usuario.save()
```

## 🔐 Verificar que Funciona

### Método 1: Probar en Django Shell

```bash
python manage.py shell
```

```python
from core.Clientes.views import autenticar_usuario

# Probar autenticación
resultado = autenticar_usuario("caty@gmail.com", "123456")

if resultado:
    print("✅ Login exitoso!")
    print(f"Usuario: {resultado}")
else:
    print("❌ Login falló")
```

### Método 2: Probar en el Navegador

1. Ir a `http://127.0.0.1:8000/login/`
2. Ingresar:
   - Email: `caty@gmail.com`
   - Password: `123456` (o la que estableciste)
3. Click en "Iniciar Sesión"
4. ✅ Debería redirigir a la tienda

## 📊 Tabla de Diagnóstico Rápido

| Síntoma | Causa Probable | Solución |
|---------|----------------|----------|
| "Password NO está hasheado" | Password en texto plano | Solución 1 |
| "No se encontró usuario" | Usuario no existe | Solución 2 |
| "Password es NULL" | Password vacío | Solución 3 |
| "Password está hasheado" pero falla | Email o password incorrectos | Solución 4 |

## 🛠️ Prevención Futura

Para evitar este problema en el futuro:

### 1. Siempre usar `make_password()` al crear usuarios

**❌ Incorrecto:**
```python
Usuario.objects.create(
    email="user@email.com",
    password="123456"  # ❌ Texto plano
)
```

**✅ Correcto:**
```python
from django.contrib.auth.hashers import make_password

Usuario.objects.create(
    email="user@email.com",
    password=make_password("123456")  # ✅ Hasheado
)
```

### 2. Usar la vista de registro

La vista `registro()` en `views.py` ya usa `make_password()` correctamente:

```python
Usuario.objects.create(
    nombre=nombre,
    email=email,
    password=make_password(password),  # ✅ Correcto
    id_rol=2,
    idCliente=nuevo_cliente.idCliente
)
```

### 3. No insertar usuarios directamente en SQL

**❌ Evitar:**
```sql
INSERT INTO usuarios (email, password) 
VALUES ('user@email.com', '123456');
```

**✅ Usar Django:**
```python
from django.contrib.auth.hashers import make_password
Usuario.objects.create(
    email="user@email.com",
    password=make_password("123456")
)
```

## 📝 Archivos Creados

1. **diagnosticar_usuario_caty.py** - Script para diagnosticar el problema
2. **arreglar_password_caty.py** - Script para arreglar el password
3. **PROBLEMA_LOGIN_CATY.md** - Este documento

## 🎯 Resumen de Pasos

1. ✅ Ejecutar `diagnosticar_usuario_caty.py`
2. ✅ Identificar el problema en la salida
3. ✅ Aplicar la solución correspondiente
4. ✅ Verificar que funciona
5. ✅ Iniciar sesión en el navegador

¡Listo! El usuario 'caty' debería poder iniciar sesión ahora. 🎉

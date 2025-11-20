# 🔧 Solución al Problema del Perfil

## 🐛 Problema Reportado

Usuario **william fontecha** (carlos@gmail.com) está viendo el formulario "Crea tu cuenta ahora" cuando **NO debería verlo** porque ya es un usuario registrado con pedidos.

## 🔍 Diagnóstico

El problema tiene dos causas posibles:

### Causa 1: Sesión Incorrecta
El usuario tiene `cliente_id` en la sesión en lugar de `usuario_id`, lo que hace que el sistema lo trate como "cliente invitado" aunque tenga usuario en la BD.

**¿Por qué pasa esto?**
- El usuario hizo pedidos como invitado (sin registrarse)
- Luego creó una cuenta o se registró
- Pero la sesión actual sigue teniendo `cliente_id` en lugar de `usuario_id`

### Causa 2: Usuario sin Vincular
El usuario existe en la tabla `usuarios` pero no tiene el campo `idCliente` correctamente vinculado.

## ✅ Soluciones Implementadas

### 1. Verificación en Base de Datos (views.py línea 70-80)

**Antes:**
```python
cliente = get_object_or_404(Cliente, idCliente=cliente_id)
tiene_usuario = False  # ❌ Siempre False para clientes invitados
sin_sesion = False
```

**Después:**
```python
cliente = get_object_or_404(Cliente, idCliente=cliente_id)

# IMPORTANTE: Verificar si este cliente ya tiene un usuario en la BD
usuario_existente = Usuario.objects.filter(idCliente=cliente.idCliente).first()
if usuario_existente:
    # El cliente ya tiene usuario, pero no está en sesión
    tiene_usuario = True  # ✅ Ahora detecta usuarios registrados
else:
    # Es un verdadero cliente invitado sin usuario
    tiene_usuario = False

sin_sesion = False
```

**Beneficio:** Ahora el sistema verifica en la base de datos si el cliente tiene un usuario asociado, incluso si la sesión no tiene `usuario_id`.

### 2. Limpieza de Sesión en Login (views.py línea 570-575)

**Antes:**
```python
if usuario:
    request.session['usuario_id'] = usuario['id']
    request.session['usuario_nombre'] = usuario['nombre']
    request.session['usuario_rol'] = usuario['rol']
```

**Después:**
```python
if usuario:
    # Limpiar cualquier sesión de cliente invitado previa
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
    if 'cliente_nombre' in request.session:
        del request.session['cliente_nombre']
    
    request.session['usuario_id'] = usuario['id']
    request.session['usuario_nombre'] = usuario['nombre']
    request.session['usuario_rol'] = usuario['rol']
```

**Beneficio:** Cuando un usuario inicia sesión, se eliminan las variables de sesión de cliente invitado para evitar conflictos.

## 🧪 Cómo Verificar la Solución

### Opción 1: Ejecutar Script de Diagnóstico

```bash
python manage.py shell < verificar_usuario.py
```

Este script te dirá:
- ✅ Si el cliente existe
- ✅ Si tiene usuario asociado
- ✅ Qué estado debería mostrar el perfil

### Opción 2: Verificación Manual en Django Shell

```bash
python manage.py shell
```

```python
from core.models import Cliente, Usuario

# Buscar el cliente
cliente = Cliente.objects.get(email="carlos@gmail.com")
print(f"Cliente ID: {cliente.idCliente}")
print(f"Nombre: {cliente.nombre}")

# Buscar si tiene usuario
usuario = Usuario.objects.filter(idCliente=cliente.idCliente).first()
if usuario:
    print(f"✅ Tiene usuario: ID {usuario.idUsuario}")
    print("NO debe ver formulario 'Crea tu cuenta ahora'")
else:
    print("❌ NO tiene usuario")
    print("DEBE ver formulario 'Crea tu cuenta ahora'")
```

### Opción 3: Probar en el Navegador

1. **Cerrar sesión completamente:**
   ```
   Ir a /logout/
   ```

2. **Iniciar sesión de nuevo:**
   ```
   Ir a /login/
   Email: carlos@gmail.com
   Contraseña: [tu contraseña]
   ```

3. **Ir al perfil:**
   ```
   Ir a /perfil/
   ```

4. **Verificar:**
   - ✅ Debe ver sus pedidos
   - ✅ Debe ver botón "Ver seguimiento" en cada pedido
   - ❌ NO debe ver formulario "Crea tu cuenta ahora"

## 🎯 Resultado Esperado

Después de estos cambios:

| Escenario | `tiene_usuario` | Ve Formulario | Explicación |
|-----------|-----------------|---------------|-------------|
| Usuario registrado con `usuario_id` en sesión | `True` | ❌ NO | Caso normal |
| Usuario registrado con `cliente_id` en sesión | `True` | ❌ NO | **Ahora detectado por verificación en BD** |
| Cliente invitado sin usuario en BD | `False` | ✅ SÍ | Caso correcto |
| Sin sesión | - | ❌ NO | Muestra mensaje de login |

## 🔄 Flujo Corregido

```
Usuario accede a /perfil/
    │
    ├─ ¿Tiene usuario_id en sesión?
    │   └─ SÍ → tiene_usuario = True ✅
    │
    └─ ¿Tiene cliente_id en sesión?
        └─ SÍ → Buscar en BD si Cliente tiene Usuario
            ├─ Usuario existe en BD → tiene_usuario = True ✅
            └─ Usuario NO existe en BD → tiene_usuario = False
```

## 📝 Archivos Modificados

1. **core/Clientes/views.py**
   - Línea 70-80: Verificación de usuario en BD
   - Línea 570-575: Limpieza de sesión en login

2. **core/Clientes/perfil/perfil.html**
   - Ya estaba correcto (solo muestra formulario si `not tiene_usuario`)

## 🚀 Próximos Pasos

1. **Ejecutar el script de diagnóstico** para confirmar el estado actual
2. **Cerrar sesión e iniciar sesión de nuevo** para limpiar la sesión
3. **Verificar que el formulario ya no aparece**

Si el problema persiste después de cerrar sesión e iniciar sesión de nuevo, ejecuta el script de diagnóstico y comparte el resultado.

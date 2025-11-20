# Lógica del Perfil - Glam Store

## 📊 Flujo de Estados del Usuario

```
┌─────────────────────────────────────────────────────────────┐
│                    VISITANTE ACCEDE A /perfil/              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ¿Tiene usuario_id en sesión?
                              │
                ┌─────────────┴─────────────┐
                │                           │
               SÍ                          NO
                │                           │
                ▼                           ▼
    ┌───────────────────────┐   ¿Tiene cliente_id en sesión?
    │  USUARIO REGISTRADO   │               │
    │  tiene_usuario = True │     ┌─────────┴─────────┐
    │  sin_sesion = False   │     │                   │
    └───────────────────────┘    SÍ                  NO
                │                 │                   │
                │                 ▼                   ▼
                │     ┌───────────────────────┐  ┌──────────────────┐
                │     │  CLIENTE INVITADO     │  │  SIN SESIÓN      │
                │     │  tiene_usuario = False│  │  sin_sesion=True │
                │     │  sin_sesion = False   │  └──────────────────┘
                │     └───────────────────────┘           │
                │                 │                       │
                └─────────────────┴───────────────────────┘
                                  │
                                  ▼
                        RENDERIZAR perfil.html
```

## 🎯 Casos de Uso

### 1️⃣ USUARIO REGISTRADO (tiene_usuario = True, sin_sesion = False)
**Características:**
- ✅ Tiene `usuario_id` en sesión
- ✅ Tiene contraseña
- ✅ Puede ver su información personal
- ✅ Puede ver sus pedidos
- ✅ Puede ver seguimiento de pedidos (botón "Ver seguimiento")
- ❌ NO ve el formulario "Crea tu cuenta ahora"

**Navegación:**
```
- Tienda
- Carrito
- Mi Perfil (activo)
- Cerrar Sesión
```

---

### 2️⃣ CLIENTE INVITADO (tiene_usuario = False, sin_sesion = False)
**Características:**
- ✅ Tiene `cliente_id` en sesión
- ✅ Hizo un pedido sin registrarse
- ✅ Puede ver su información personal
- ✅ Puede ver sus pedidos
- ❌ NO puede ver seguimiento de pedidos
- ✅ VE el formulario "Crea tu cuenta ahora" ← IMPORTANTE

**Navegación:**
```
- Tienda
- Carrito
- Mi Perfil (activo)
- Cerrar Sesión de Invitado
```

**Formulario mostrado:**
```
┌─────────────────────────────────────────────┐
│ Crea tu cuenta ahora                        │
│                                             │
│ Actualmente eres un cliente invitado       │
│                                             │
│ Correo: [email@ejemplo.com] (readonly)     │
│ Crear contraseña: [______]                 │
│ Confirmar contraseña: [______]             │
│                                             │
│ [Crear mi cuenta ahora]                    │
└─────────────────────────────────────────────┘
```

---

### 3️⃣ SIN SESIÓN (sin_sesion = True)
**Características:**
- ❌ NO tiene `usuario_id` en sesión
- ❌ NO tiene `cliente_id` en sesión
- ❌ No ha hecho pedidos
- ❌ NO puede ver información personal
- ❌ NO puede ver pedidos
- ❌ NO ve el formulario "Crea tu cuenta ahora"
- ✅ Ve mensaje para iniciar sesión/registrarse

**Navegación:**
```
- Tienda
- Carrito
- Iniciar Sesión
- Registrarse
```

**Mensaje mostrado:**
```
┌─────────────────────────────────────────────┐
│ Acceso al Perfil                            │
│                                             │
│ Para ver tu perfil, necesitas hacer un     │
│ pedido, registrarte o iniciar sesión.      │
│                                             │
│ [Ir a la Tienda] [Registrarse] [Iniciar]  │
└─────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Conversión: Invitado → Usuario Registrado

```
1. Cliente hace pedido sin registrarse
   └─> Se crea Cliente en BD
   └─> Se guarda cliente_id en sesión
   └─> tiene_usuario = False

2. Cliente accede a /perfil/
   └─> Ve sus pedidos
   └─> Ve formulario "Crea tu cuenta ahora"

3. Cliente completa formulario
   └─> POST a /crear-usuario-desde-cliente/
   └─> Se crea Usuario vinculado al Cliente
   └─> Se guarda usuario_id en sesión
   └─> Se elimina cliente_id de sesión
   └─> tiene_usuario = True

4. Cliente ahora es Usuario Registrado
   └─> Ya NO ve el formulario
   └─> Puede ver seguimiento de pedidos
```

---

## 🔐 Variables de Sesión

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `usuario_id` | int | ID del usuario registrado (tiene contraseña) |
| `cliente_id` | int | ID del cliente invitado (sin contraseña) |
| `usuario_nombre` | str | Nombre del usuario/cliente |
| `usuario_rol` | int | Rol del usuario (1=Admin, 2=Cliente) |

---

## ✅ Resumen de Cambios Realizados

### Antes (❌ Problema):
- Usaba `user.is_authenticated` (siempre False)
- El formulario aparecía para todos los usuarios sin sesión
- Navegación confusa con opciones duplicadas

### Después (✅ Solución):
- Usa `sin_sesion`, `tiene_usuario` correctamente
- El formulario SOLO aparece para clientes invitados
- Navegación clara según el estado del usuario
- Tres estados bien diferenciados

---

## 🧪 Cómo Probar

### Probar Usuario Registrado:
1. Ir a `/registro/`
2. Crear cuenta con email y contraseña
3. Ir a `/perfil/`
4. ✅ Debe ver sus datos
5. ❌ NO debe ver "Crea tu cuenta ahora"

### Probar Cliente Invitado:
1. Agregar productos al carrito
2. Ir a checkout
3. Completar datos SIN registrarse
4. Finalizar pedido
5. Ir a `/perfil/`
6. ✅ Debe ver sus datos y pedidos
7. ✅ DEBE ver "Crea tu cuenta ahora"

### Probar Sin Sesión:
1. Abrir navegador en modo incógnito
2. Ir directamente a `/perfil/`
3. ✅ Debe ver mensaje "Acceso al Perfil"
4. ❌ NO debe ver datos personales
5. ❌ NO debe ver "Crea tu cuenta ahora"

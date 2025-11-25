# 📦 RESUMEN DEL PROYECTO GLAMSTORE

## 🎯 Descripción General

**Glamstore** es una plataforma de e-commerce Django para gestión de pedidos, clientes, productos y entregas. El sistema está diseñado para coordinar repartidores, gestionar inventario y facilitar el seguimiento de pedidos.

---

## 🏗️ Arquitectura del Proyecto

### Estructura Principal
```
glamstore/
├── core/                          # Aplicación principal Django
│   ├── models/                    # Modelos de datos
│   │   ├── pedidos.py            # Pedido, DetallePedido, PedidoProducto
│   │   ├── clientes.py           # Cliente
│   │   ├── repartidores.py       # Repartidor
│   │   └── ...otros modelos
│   ├── Clientes/                 # Vistas y templates para clientes
│   │   ├── views.py              # Lógica de cliente
│   │   ├── services.py           # Servicios de cliente
│   │   ├── carrito/              # Carrito de compras
│   │   ├── pedido_confirmado/    # Confirmación de pedido
│   │   ├── perfil/               # Perfil del cliente
│   │   ├── seguimiento_pedidos/  # Seguimiento y checkout
│   │   └── ...otros módulos
│   ├── Gestion_admin/            # Vistas y templates para admin
│   │   ├── views.py              # Lógica del admin
│   │   ├── services_repartidores.py  # Servicios de repartidores
│   │   ├── Panel_pedidos/        # Gestión de pedidos
│   │   ├── Panel_repartidores/   # Gestión de repartidores
│   │   ├── Panel_productos/      # Gestión de productos
│   │   ├── Panel_cliente/        # Gestión de clientes
│   │   └── ...otros paneles
│   ├── static/                   # Archivos estáticos (CSS, JS)
│   ├── migrations/               # Migraciones de BD
│   └── management/               # Comandos personalizados
├── glamstore/                     # Configuración Django
│   ├── settings.py               # Configuración del proyecto
│   ├── urls.py                   # URLs principales
│   └── wsgi.py
├── manage.py                      # Utilidad de Django
├── .env                          # Variables de entorno
└── requirements.txt              # Dependencias Python
```

---

## 📊 Modelos de Datos Principales

### 1. **Pedido** (`core/models/pedidos.py`)
```python
- idPedido (PK)
- fechaCreacion (DateTime)
- estado (CharField) - Confirmado, En Preparación, En Camino, Entregado, Completado, Problema en Entrega
- estado_pago (CharField) - Pago Completo, Pago Parcial
- estado_pedido (CharField) - Estados del pedido
- total (DecimalField)
- idCliente (FK → Cliente)
- idRepartidor (FK → Repartidor, nullable)
- fecha_vencimiento (DateField, nullable) - ✨ NUEVO
```

### 2. **Cliente** (`core/models/clientes.py`)
```python
- idCliente (PK)
- cedula (CharField)
- nombre (CharField)
- email (CharField, unique)
- direccion (CharField)
- telefono (CharField)
```

### 3. **Repartidor** (`core/models/repartidores.py`)
```python
- idRepartidor (PK)
- nombreRepartidor (CharField)
- telefono (CharField)
- email (EmailField) - ✨ NUEVO
- estado_turno (CharField) - Disponible, etc.
```

### 4. **DetallePedido** (`core/models/pedidos.py`)
```python
- idDetalle (PK)
- idPedido (FK → Pedido)
- idProducto (FK → Producto)
- cantidad (PositiveIntegerField)
- precio_unitario (DecimalField)
- subtotal (DecimalField)
```

---

## 🔧 Funcionalidades Principales

### 1. **Gestión de Pedidos**
- Crear, editar, eliminar pedidos
- Asignar repartidores automáticamente
- Cambiar estado de pedidos
- Calcular totales con IVA
- Soporte para pago completo y parcial

### 2. **Gestión de Repartidores**
- Crear y editar repartidores
- Asignar pedidos automáticamente
- Enviar correos con rutas de entrega
- Generar PDFs con información de pedidos
- Calcular capacidad de repartidores

### 3. **Gestión de Clientes**
- Registro y login de clientes
- Perfil de cliente
- Historial de pedidos
- Seguimiento de pedidos
- Notificaciones

### 4. **Gestión de Productos**
- Crear, editar, eliminar productos
- Gestionar categorías y subcategorías
- Controlar inventario
- Movimientos de productos

### 5. **Sistema de Vencimiento** ✨ NUEVO
- Cálculo automático de fecha de vencimiento
- Bogotá: 2 días hábiles
- Soacha: 3 días hábiles
- Alertas visuales en correos y PDFs
- Estados: 🔴 VENCE HOY, ⚠️ Vence en X días, ❌ VENCIDO

---

## 📧 Servicios de Correo

### `services_repartidores.py` - Funciones Principales

#### 1. **`calcular_fecha_vencimiento(fecha_pedido, ciudad)`**
- Calcula la fecha de vencimiento según la ciudad
- Bogotá: 2 días hábiles
- Soacha: 3 días hábiles
- Solo cuenta lunes a viernes

#### 2. **`enviar_correo_repartidor_detallado(repartidor, fecha=None)`**
- Envía correo HTML con tabla de pedidos
- Incluye información de vencimiento
- Adjunta PDF con ruta de entregas
- Muestra alertas visuales de urgencia

#### 3. **`generar_pdf_pedidos_repartidor(repartidor, fecha=None)`**
- Genera PDF con todos los pedidos pendientes
- Incluye información de vencimiento
- Formato imprimible
- Tabla con detalles de clientes y direcciones

#### 4. **`asignar_pedidos_automaticamente(fecha=None)`**
- Asigna pedidos a repartidores disponibles
- Respeta capacidad de repartidores (4 pedidos máximo)
- Horario: 6 AM - 3 PM (2 horas por pedido)
- Agenda pedidos para el día siguiente si no hay capacidad

#### 5. **`calcular_capacidad_repartidor(repartidor, fecha=None)`**
- Calcula cuántos pedidos más puede tomar un repartidor
- Máximo 4 pedidos por día
- Basado en horario de 6 AM a 3 PM

---

## 🎨 Vistas Principales

### Admin (`core/Gestion_admin/views.py`)
- **Dashboard**: Estadísticas generales
- **Panel de Pedidos**: Listar, crear, editar, eliminar pedidos
- **Panel de Repartidores**: Gestionar repartidores y asignaciones
- **Panel de Productos**: Gestionar catálogo
- **Panel de Clientes**: Gestionar clientes
- **Panel de Categorías**: Gestionar categorías y subcategorías

### Cliente (`core/Clientes/views.py`)
- **Tienda**: Listar productos
- **Carrito**: Gestionar carrito de compras
- **Checkout**: Realizar compra
- **Pedido Confirmado**: Confirmación de pedido
- **Seguimiento**: Seguimiento de pedidos
- **Perfil**: Información del cliente
- **Notificaciones**: Notificaciones del cliente

---

## 📋 Templates Principales

### Admin
```
core/Gestion_admin/
├── Panel_pedidos/
│   ├── lista_pedidos.html
│   ├── pedidos_detalle.html
│   ├── pedidos_editar.html
│   └── pedido_pdf_template.html
├── Panel_repartidores/
│   ├── lista_repartidores.html
│   ├── repartidores_agregar.html
│   ├── repartidores_editar.html
│   ├── asignacion_pedido_pdf.html
│   └── asignacion_pedidos_repartidor_pdf.html
├── Panel_productos/
│   ├── lista_productos.html
│   ├── productos_agregar.html
│   ├── productos_editar.html
│   └── productos_detalle.html
└── ...otros paneles
```

### Cliente
```
core/Clientes/
├── tienda/
│   └── tienda.html
├── carrito/
│   └── carrito.html
├── seguimiento_pedidos/
│   └── checkout.html
├── pedido_confirmado/
│   ├── pedido_confirmado.html
│   └── ver_seguimiento.html
├── perfil/
│   ├── perfil.html
│   ├── notificaciones_cliente.html
│   ├── confirmar_recepcion.html
│   └── reportar_problema.html
└── ...otros módulos
```

---

## 🔐 Configuración

### `.env`
```
PYTHONPATH=core
SECRET_KEY='django-insecure-...'
EMAIL_HOST_USER='glamstore0303777@gmail.com'
EMAIL_HOST_PASSWORD='lyuuvczxwhbljttc'
```

### Configuración de Email
- **Host**: Gmail
- **Puerto**: 587 (TLS)
- **Usuario**: glamstore0303777@gmail.com
- **Contraseña**: Contraseña de aplicación

---

## 📊 Flujo de Pedidos

```
1. Cliente crea pedido en tienda
   ↓
2. Pedido se guarda con estado "Confirmado"
   ↓
3. Admin asigna repartidor (automático o manual)
   ↓
4. Sistema calcula fecha de vencimiento
   ↓
5. Se envía correo al repartidor con ruta
   ↓
6. Repartidor entrega pedido
   ↓
7. Cliente confirma recepción
   ↓
8. Pedido se marca como "Completado"
```

---

## 🚀 Características Implementadas

✅ **Sistema de Vencimiento**
- Cálculo automático según ciudad
- Alertas visuales en correos y PDFs
- Información de días restantes

✅ **Correos Detallados**
- Tabla con información completa de pedidos
- Incluye fecha de vencimiento
- Alertas de urgencia
- PDF adjunto con ruta

✅ **Gestión de Repartidores**
- Asignación automática de pedidos
- Cálculo de capacidad
- Envío de correos con rutas
- Generación de PDFs

✅ **Gestión de Pedidos**
- Estados de pedido y pago
- Seguimiento de pedidos
- Información de vencimiento
- Alertas visuales

---

## 📝 Archivos de Prueba y Utilidades

El proyecto incluye varios scripts de prueba y utilidades:

- `test_boton_web.py` - Pruebas del botón web
- `test_envio_correos.py` - Pruebas de envío de correos
- `test_pdf_pago_parcial_final.py` - Pruebas de PDF
- `calcular_fecha_vencimiento.py` - Cálculo de vencimientos
- `crear_pedidos_prueba.py` - Crear pedidos de prueba
- `verificar_pedidos_parciales.py` - Verificar pedidos parciales
- Y muchos más...

---

## 🔄 Próximos Pasos

1. **Confirmar Recepción del Cliente**
   - Vista para que cliente confirme recepción
   - Cambiar estado a "Completado"
   - Notificación al repartidor

2. **Reportar Problemas**
   - Vista para reportar problemas en entrega
   - Cambiar estado a "Problema en Entrega"
   - Notificación al admin

3. **Mejoras en Seguimiento**
   - Mapa de ruta en tiempo real
   - Notificaciones push
   - Historial de entregas

4. **Optimización de Rutas**
   - Algoritmo de optimización de rutas
   - Cálculo de distancias
   - Estimación de tiempos

---

## 📞 Contacto y Soporte

- **Email**: glamstore0303777@gmail.com
- **Soporte**: soporte@glamstore.com

---

**Última actualización**: 24/11/2025  
**Estado**: En desarrollo activo

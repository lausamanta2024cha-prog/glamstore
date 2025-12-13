# Glam Store - E-commerce Platform

Plataforma de e-commerce para Glam Store, desarrollada con Django y MySQL.

## Características

- Gestión de productos y categorías
- Carrito de compras
- Sistema de pedidos
- Gestión de repartidores
- Seguimiento de pedidos
- Sistema de notificaciones
- Panel de administración

## Requisitos

- Python 3.13+
- MySQL 8.0+
- pip

## Instalación Local

1. Clonar el repositorio:
```bash
git clone https://github.com/lausamanta2024cha-prog/glamstore.git
cd glamstore
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus valores
```

5. Ejecutar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Ejecutar servidor de desarrollo:
```bash
python manage.py runserver
```

## Despliegue en Railway

### Requisitos previos:
- Cuenta en [Railway.app](https://railway.app)
- Repositorio en GitHub

### Pasos:

1. Conectar repositorio a Railway
2. Configurar variables de entorno en Railway:
   - `SECRET_KEY`: Clave secreta de Django
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: Tu dominio en Railway
   - `DATABASE_URL`: URL de conexión a MySQL (Railway la proporciona)
   - `EMAIL_HOST_PASSWORD`: Contraseña de aplicación de Gmail

3. Railway ejecutará automáticamente:
   - Instalación de dependencias
   - Migraciones de base de datos
   - Recolección de archivos estáticos
   - Inicio de Gunicorn

## Estructura del Proyecto

```
glamstore/
├── core/                    # Aplicación principal
│   ├── Clientes/           # Vistas y templates para clientes
│   ├── Gestion_admin/      # Vistas y templates para administración
│   ├── models/             # Modelos de datos
│   ├── migrations/         # Migraciones de BD
│   └── static/             # Archivos estáticos
├── glamstore/              # Configuración del proyecto
├── requirements.txt        # Dependencias
├── Dockerfile             # Configuración Docker
├── Procfile               # Configuración para Railway
└── railway.json           # Configuración específica de Railway
```

## Base de Datos

El proyecto usa MySQL con los siguientes modelos principales:

- **Usuario**: Usuarios del sistema (clientes y administradores)
- **Cliente**: Información de clientes
- **Producto**: Catálogo de productos
- **Pedido**: Órdenes de compra
- **Repartidor**: Gestión de repartidores
- **Notificación**: Sistema de notificaciones

## Configuración de Email

El proyecto usa Gmail para enviar correos. Para configurar:

1. Habilitar autenticación de dos factores en tu cuenta de Gmail
2. Generar una contraseña de aplicación
3. Configurar `EMAIL_HOST_PASSWORD` con la contraseña generada

## Licencia

Proyecto privado de Glam Store

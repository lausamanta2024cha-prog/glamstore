# 🚀 GUÍA DE DESARROLLO - GLAMSTORE

## 📋 Tabla de Contenidos
1. [Configuración Inicial](#configuración-inicial)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Convenciones de Código](#convenciones-de-código)
4. [Flujo de Desarrollo](#flujo-de-desarrollo)
5. [Pruebas](#pruebas)
6. [Despliegue](#despliegue)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Configuración Inicial

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd glamstore
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Crear archivo .env en la raíz del proyecto
PYTHONPATH=core
SECRET_KEY='tu-clave-secreta-aqui'
EMAIL_HOST_USER='tu-email@gmail.com'
EMAIL_HOST_PASSWORD='tu-contraseña-de-aplicacion'
DATABASE_URL='mysql://usuario:contraseña@localhost:3306/glamstoredb'
```

### 5. Configurar Base de Datos
```bash
# Crear base de datos
mysql -u root -p
CREATE DATABASE glamstoredb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Aplicar migraciones
python manage.py migrate
```

### 6. Crear Superusuario
```bash
python manage.py createsuperuser
```

### 7. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

Acceder a: http://localhost:8000

---

## 📁 Estructura del Proyecto

### Carpetas Principales

```
glamstore/
├── core/                          # Aplicación principal
│   ├── models/                    # Modelos de datos
│   │   ├── __init__.py
│   │   ├── pedidos.py            # Pedido, DetallePedido, PedidoProducto
│   │   ├── clientes.py           # Cliente
│   │   ├── repartidores.py       # Repartidor
│   │   ├── productos.py          # Producto, Categoría, Subcategoría
│   │   ├── usuarios.py           # Usuario
│   │   ├── distribuidores.py     # Distribuidor
│   │   └── movimientos.py        # MovimientoProducto
│   │
│   ├── Clientes/                 # Vistas y templates para clientes
│   │   ├── views.py              # Lógica de cliente
│   │   ├── services.py           # Servicios de cliente
│   │   ├── forms.py              # Formularios de cliente
│   │   ├── urls.py               # URLs de cliente
│   │   ├── carrito/              # Carrito de compras
│   │   ├── pedido_confirmado/    # Confirmación de pedido
│   │   ├── perfil/               # Perfil del cliente
│   │   ├── seguimiento_pedidos/  # Seguimiento y checkout
│   │   ├── tienda/               # Tienda principal
│   │   ├── registrar_usuario/    # Registro y login
│   │   └── productos_categoria/  # Productos por categoría
│   │
│   ├── Gestion_admin/            # Vistas y templates para admin
│   │   ├── views.py              # Lógica del admin
│   │   ├── services_repartidores.py  # Servicios de repartidores
│   │   ├── forms.py              # Formularios del admin
│   │   ├── urls.py               # URLs del admin
│   │   ├── Panel_pedidos/        # Gestión de pedidos
│   │   ├── Panel_repartidores/   # Gestión de repartidores
│   │   ├── Panel_productos/      # Gestión de productos
│   │   ├── Panel_cliente/        # Gestión de clientes
│   │   ├── Panel_categorias/     # Gestión de categorías
│   │   ├── Panel_distribuidores/ # Gestión de distribuidores
│   │   ├── Panel_admin/          # Gestión de admins
│   │   └── Admin/                # Dashboard del admin
│   │
│   ├── static/                   # Archivos estáticos
│   │   ├── css/                  # Estilos CSS
│   │   ├── js/                   # Scripts JavaScript
│   │   └── images/               # Imágenes
│   │
│   ├── migrations/               # Migraciones de BD
│   ├── management/               # Comandos personalizados
│   ├── templatetags/             # Template tags personalizados
│   ├── admin.py                  # Configuración del admin de Django
│   ├── apps.py                   # Configuración de la app
│   ├── models.py                 # Importación de modelos
│   ├── views.py                  # Vistas principales
│   ├── tests.py                  # Pruebas
│   └── urls.py                   # URLs principales
│
├── glamstore/                     # Configuración Django
│   ├── settings.py               # Configuración del proyecto
│   ├── urls.py                   # URLs principales
│   ├── wsgi.py                   # WSGI para producción
│   └── asgi.py                   # ASGI para WebSockets
│
├── media/                        # Archivos subidos por usuarios
├── templates/                    # Templates base
├── manage.py                     # Utilidad de Django
├── requirements.txt              # Dependencias Python
├── .env                         # Variables de entorno
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Documentación del proyecto
```

---

## 📝 Convenciones de Código

### 1. Nombres de Variables
```python
# ✅ Correcto
nombre_cliente = "Juan"
fecha_vencimiento = datetime.now()
es_pagado = True
total_pedidos = 10

# ❌ Incorrecto
nombreCliente = "Juan"
FechaVencimiento = datetime.now()
isPagado = True
totalPedidos = 10
```

### 2. Nombres de Funciones
```python
# ✅ Correcto
def calcular_fecha_vencimiento(fecha_pedido, ciudad):
    pass

def enviar_correo_repartidor(repartidor):
    pass

def obtener_pedidos_sin_asignar(fecha):
    pass

# ❌ Incorrecto
def CalcularFechaVencimiento(fecha_pedido, ciudad):
    pass

def enviarCorreoRepartidor(repartidor):
    pass

def ObtenerPedidosSinAsignar(fecha):
    pass
```

### 3. Nombres de Clases
```python
# ✅ Correcto
class Pedido(models.Model):
    pass

class ClienteForm(forms.ModelForm):
    pass

class RepartidorService:
    pass

# ❌ Incorrecto
class pedido(models.Model):
    pass

class cliente_form(forms.ModelForm):
    pass

class repartidor_service:
    pass
```

### 4. Constantes
```python
# ✅ Correcto
HORARIO_INICIO = 6
HORARIO_FIN = 15
TIEMPO_ENTREGA_MINUTOS = 120
PEDIDOS_POR_REPARTIDOR = 4

# ❌ Incorrecto
horario_inicio = 6
horarioFin = 15
tiempo_entrega = 120
pedidosPorRepartidor = 4
```

### 5. Comentarios
```python
# ✅ Correcto
def calcular_fecha_vencimiento(fecha_pedido, ciudad):
    """
    Calcula la fecha de vencimiento según la ciudad.
    
    Args:
        fecha_pedido (datetime): Fecha de creación del pedido
        ciudad (str): Ciudad de entrega (Bogotá o Soacha)
    
    Returns:
        datetime: Fecha de vencimiento calculada
    """
    dias_vencimiento = 2 if 'bogota' in ciudad.lower() else 3
    # ... resto del código

# ❌ Incorrecto
def calcular_fecha_vencimiento(fecha_pedido, ciudad):
    # Calcular vencimiento
    dias_vencimiento = 2 if 'bogota' in ciudad.lower() else 3
    # ... resto del código
```

### 6. Indentación
```python
# ✅ Correcto (4 espacios)
def mi_funcion():
    if condicion:
        hacer_algo()
        hacer_otra_cosa()

# ❌ Incorrecto (2 espacios o tabs)
def mi_funcion():
  if condicion:
    hacer_algo()
    hacer_otra_cosa()
```

---

## 🔄 Flujo de Desarrollo

### 1. Crear una Nueva Funcionalidad

#### Paso 1: Crear rama
```bash
git checkout -b feature/nombre-funcionalidad
```

#### Paso 2: Crear modelo (si es necesario)
```python
# core/models/nueva_funcionalidad.py
from django.db import models

class NuevaFuncionalidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'nueva_funcionalidad'
        managed = False
        app_label = 'core'
    
    def __str__(self):
        return self.nombre
```

#### Paso 3: Crear migración
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Paso 4: Crear vista
```python
# core/Clientes/views.py o core/Gestion_admin/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def nueva_funcionalidad_view(request):
    """Vista para nueva funcionalidad"""
    if request.method == 'POST':
        # Procesar formulario
        pass
    
    # Obtener datos
    datos = {}
    
    return render(request, 'template.html', datos)
```

#### Paso 5: Crear formulario
```python
# core/Clientes/forms.py o core/Gestion_admin/forms.py
from django import forms
from core.models.nueva_funcionalidad import NuevaFuncionalidad

class NuevaFuncionalidadForm(forms.ModelForm):
    class Meta:
        model = NuevaFuncionalidad
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
```

#### Paso 6: Crear template
```html
<!-- core/Clientes/nueva_funcionalidad/nueva_funcionalidad.html -->
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h1>Nueva Funcionalidad</h1>
    
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Guardar</button>
    </form>
</div>
{% endblock %}
```

#### Paso 7: Crear URL
```python
# core/Clientes/urls.py o core/Gestion_admin/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('nueva-funcionalidad/', views.nueva_funcionalidad_view, name='nueva_funcionalidad'),
]
```

#### Paso 8: Crear pruebas
```python
# core/tests.py
from django.test import TestCase
from core.models.nueva_funcionalidad import NuevaFuncionalidad

class NuevaFuncionalidadTestCase(TestCase):
    def setUp(self):
        NuevaFuncionalidad.objects.create(
            nombre="Test",
            descripcion="Descripción de prueba"
        )
    
    def test_crear_nueva_funcionalidad(self):
        obj = NuevaFuncionalidad.objects.get(nombre="Test")
        self.assertEqual(obj.descripcion, "Descripción de prueba")
```

#### Paso 9: Hacer commit
```bash
git add .
git commit -m "feat: agregar nueva funcionalidad"
```

#### Paso 10: Hacer push
```bash
git push origin feature/nombre-funcionalidad
```

#### Paso 11: Crear Pull Request
- Ir a GitHub
- Crear Pull Request
- Describir cambios
- Esperar revisión

---

## 🧪 Pruebas

### 1. Ejecutar Todas las Pruebas
```bash
python manage.py test
```

### 2. Ejecutar Pruebas de una App
```bash
python manage.py test core
```

### 3. Ejecutar Pruebas de un Archivo
```bash
python manage.py test core.tests.NuevaFuncionalidadTestCase
```

### 4. Ejecutar Pruebas con Verbosidad
```bash
python manage.py test --verbosity=2
```

### 5. Crear Pruebas
```python
# core/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from core.models.clientes import Cliente
from core.models.pedidos import Pedido

class ClienteTestCase(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            cedula="1234567890",
            nombre="Juan",
            email="juan@example.com",
            direccion="Calle 1",
            telefono="3001234567"
        )
    
    def test_crear_cliente(self):
        self.assertEqual(self.cliente.nombre, "Juan")
    
    def test_cliente_email_unico(self):
        with self.assertRaises(Exception):
            Cliente.objects.create(
                cedula="0987654321",
                nombre="Pedro",
                email="juan@example.com",
                direccion="Calle 2",
                telefono="3009876543"
            )

class PedidoTestCase(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            cedula="1234567890",
            nombre="Juan",
            email="juan@example.com",
            direccion="Bogotá",
            telefono="3001234567"
        )
        self.pedido = Pedido.objects.create(
            fechaCreacion=timezone.now(),
            estado_pago='Pago Completo',
            estado_pedido='Confirmado',
            total=100000,
            idCliente=self.cliente
        )
    
    def test_crear_pedido(self):
        self.assertEqual(self.pedido.total, 100000)
    
    def test_calcular_fecha_vencimiento(self):
        from core.Gestion_admin.services_repartidores import calcular_fecha_vencimiento
        fecha_vencimiento = calcular_fecha_vencimiento(
            self.pedido.fechaCreacion.date(),
            'Bogotá'
        )
        self.assertIsNotNone(fecha_vencimiento)
```

---

## 🚀 Despliegue

### 1. Preparar para Producción

#### Actualizar settings.py
```python
# glamstore/settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Configurar base de datos de producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'glamstore_prod',
        'USER': 'usuario_prod',
        'PASSWORD': 'contraseña_prod',
        'HOST': 'servidor-bd.com',
        'PORT': '3306',
    }
}

# Configurar email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

### 2. Recopilar Archivos Estáticos
```bash
python manage.py collectstatic --noinput
```

### 3. Crear Archivo de Requisitos
```bash
pip freeze > requirements.txt
```

### 4. Desplegar en Servidor

#### Opción 1: Heroku
```bash
# Instalar Heroku CLI
# Crear archivo Procfile
web: gunicorn glamstore.wsgi

# Crear archivo runtime.txt
python-3.9.0

# Desplegar
heroku login
heroku create nombre-app
git push heroku main
heroku run python manage.py migrate
```

#### Opción 2: AWS
```bash
# Crear instancia EC2
# Instalar dependencias
sudo apt-get update
sudo apt-get install python3-pip python3-venv mysql-server

# Clonar repositorio
git clone <url>
cd glamstore

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
nano .env

# Ejecutar migraciones
python manage.py migrate

# Ejecutar servidor
gunicorn glamstore.wsgi:application --bind 0.0.0.0:8000
```

---

## 🔧 Troubleshooting

### 1. Error: "No module named 'core'"
**Solución**: Asegúrate de que `PYTHONPATH=core` está en `.env`

### 2. Error: "ModuleNotFoundError: No module named 'django'"
**Solución**: Instala las dependencias
```bash
pip install -r requirements.txt
```

### 3. Error: "django.db.utils.OperationalError: (1045, "Access denied for user")"
**Solución**: Verifica las credenciales de la base de datos en `.env`

### 4. Error: "SMTPAuthenticationError"
**Solución**: Verifica que estés usando una contraseña de aplicación de Gmail, no la contraseña de la cuenta

### 5. Error: "TemplateDoesNotExist"
**Solución**: Verifica que el template existe en la carpeta correcta y que `TEMPLATES` está configurado en `settings.py`

### 6. Error: "CSRF token missing or incorrect"
**Solución**: Asegúrate de incluir `{% csrf_token %}` en los formularios

### 7. Error: "No such table"
**Solución**: Ejecuta las migraciones
```bash
python manage.py migrate
```

### 8. Error: "Static files not found"
**Solución**: Recopila los archivos estáticos
```bash
python manage.py collectstatic
```

---

## 📚 Recursos Útiles

- [Documentación de Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap](https://getbootstrap.com/)
- [MySQL](https://dev.mysql.com/doc/)
- [Git](https://git-scm.com/doc)

---

**Última actualización**: 24/11/2025  
**Versión**: 1.0

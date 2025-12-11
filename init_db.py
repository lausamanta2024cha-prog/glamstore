#!/usr/bin/env python
import os
import django
from django.conf import settings
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

# SQL para crear todas las tablas (compatible con PostgreSQL y SQLite)
CREATE_TABLES_SQL_POSTGRES = """
DROP TABLE IF EXISTS movimientos_lote CASCADE;
DROP TABLE IF EXISTS lotes_producto CASCADE;
DROP TABLE IF EXISTS detallepedido CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS subcategorias CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;

CREATE TABLE categorias (
    idCategoria SERIAL PRIMARY KEY,
    nombreCategoria VARCHAR(20) NOT NULL,
    descripcion TEXT,
    imagen VARCHAR(100)
);

CREATE TABLE subcategorias (
    idSubcategoria SERIAL PRIMARY KEY,
    nombreSubcategoria VARCHAR(50) NOT NULL,
    descripcion TEXT,
    idCategoria INTEGER REFERENCES categorias(idCategoria) ON DELETE CASCADE
);

CREATE TABLE productos (
    idProducto BIGSERIAL PRIMARY KEY,
    nombreProducto VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    descripcion TEXT,
    lote VARCHAR(100),
    cantidadDisponible INTEGER DEFAULT 0,
    fechaIngreso TIMESTAMP,
    fechaVencimiento DATE,
    idCategoria INTEGER REFERENCES categorias(idCategoria) ON DELETE SET NULL,
    idSubcategoria INTEGER REFERENCES subcategorias(idSubcategoria) ON DELETE SET NULL,
    imagen VARCHAR(100),
    precio_venta DECIMAL(10, 2) DEFAULT 0
);

CREATE TABLE clientes (
    idCliente BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cedula VARCHAR(20),
    telefono VARCHAR(20),
    direccion TEXT
);

CREATE TABLE pedidos (
    idPedido BIGSERIAL PRIMARY KEY,
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'En Preparacion',
    estado_pedido VARCHAR(50) DEFAULT 'En Preparacion',
    estado_pago VARCHAR(50) DEFAULT 'Pendiente',
    total DECIMAL(10, 2) DEFAULT 0,
    idCliente BIGINT NOT NULL REFERENCES clientes(idCliente) ON DELETE CASCADE,
    fecha_vencimiento DATE,
    idRepartidor INTEGER,
    facturas_enviadas INTEGER DEFAULT 0
);

CREATE TABLE detallepedido (
    idDetallePedido BIGSERIAL PRIMARY KEY,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    margen_ganancia DECIMAL(5, 2) DEFAULT 0,
    idPedido BIGINT NOT NULL REFERENCES pedidos(idPedido) ON DELETE CASCADE,
    idProducto BIGINT NOT NULL REFERENCES productos(idProducto) ON DELETE CASCADE
);

CREATE TABLE lotes_producto (
    idLote SERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES productos(idProducto) ON DELETE CASCADE,
    codigo_lote VARCHAR(100) NOT NULL,
    fecha_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento DATE,
    cantidad_inicial INTEGER NOT NULL,
    cantidad_disponible INTEGER NOT NULL,
    costo_unitario DECIMAL(10, 2) DEFAULT 0,
    precio_venta DECIMAL(10, 2) DEFAULT 0,
    total_con_iva DECIMAL(10, 2),
    iva DECIMAL(10, 2),
    proveedor VARCHAR(200),
    UNIQUE(producto_id, codigo_lote)
);

CREATE TABLE movimientos_lote (
    idMovimientoLote SERIAL PRIMARY KEY,
    lote_id INTEGER NOT NULL REFERENCES lotes_producto(idLote) ON DELETE CASCADE,
    movimiento_producto_id INTEGER,
    cantidad INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TABLES_SQL_SQLITE = """
DROP TABLE IF EXISTS movimientos_lote;
DROP TABLE IF EXISTS lotes_producto;
DROP TABLE IF EXISTS detallepedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS subcategorias;
DROP TABLE IF EXISTS categorias;

CREATE TABLE categorias (
    idCategoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombreCategoria VARCHAR(20) NOT NULL,
    descripcion TEXT,
    imagen VARCHAR(100)
);

CREATE TABLE subcategorias (
    idSubcategoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombreSubcategoria VARCHAR(50) NOT NULL,
    descripcion TEXT,
    idCategoria INTEGER REFERENCES categorias(idCategoria) ON DELETE CASCADE
);

CREATE TABLE productos (
    idProducto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombreProducto VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    descripcion TEXT,
    lote VARCHAR(100),
    cantidadDisponible INTEGER DEFAULT 0,
    fechaIngreso TIMESTAMP,
    fechaVencimiento DATE,
    idCategoria INTEGER REFERENCES categorias(idCategoria) ON DELETE SET NULL,
    idSubcategoria INTEGER REFERENCES subcategorias(idSubcategoria) ON DELETE SET NULL,
    imagen VARCHAR(100),
    precio_venta DECIMAL(10, 2) DEFAULT 0
);

CREATE TABLE clientes (
    idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cedula VARCHAR(20),
    telefono VARCHAR(20),
    direccion TEXT
);

CREATE TABLE pedidos (
    idPedido INTEGER PRIMARY KEY AUTOINCREMENT,
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'En Preparacion',
    estado_pedido VARCHAR(50) DEFAULT 'En Preparacion',
    estado_pago VARCHAR(50) DEFAULT 'Pendiente',
    total DECIMAL(10, 2) DEFAULT 0,
    idCliente INTEGER NOT NULL REFERENCES clientes(idCliente) ON DELETE CASCADE,
    fecha_vencimiento DATE,
    idRepartidor INTEGER,
    facturas_enviadas INTEGER DEFAULT 0
);

CREATE TABLE detallepedido (
    idDetallePedido INTEGER PRIMARY KEY AUTOINCREMENT,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    margen_ganancia DECIMAL(5, 2) DEFAULT 0,
    idPedido INTEGER NOT NULL REFERENCES pedidos(idPedido) ON DELETE CASCADE,
    idProducto INTEGER NOT NULL REFERENCES productos(idProducto) ON DELETE CASCADE
);

CREATE TABLE lotes_producto (
    idLote INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL REFERENCES productos(idProducto) ON DELETE CASCADE,
    codigo_lote VARCHAR(100) NOT NULL,
    fecha_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento DATE,
    cantidad_inicial INTEGER NOT NULL,
    cantidad_disponible INTEGER NOT NULL,
    costo_unitario DECIMAL(10, 2) DEFAULT 0,
    precio_venta DECIMAL(10, 2) DEFAULT 0,
    total_con_iva DECIMAL(10, 2),
    iva DECIMAL(10, 2),
    proveedor VARCHAR(200),
    UNIQUE(producto_id, codigo_lote)
);

CREATE TABLE movimientos_lote (
    idMovimientoLote INTEGER PRIMARY KEY AUTOINCREMENT,
    lote_id INTEGER NOT NULL REFERENCES lotes_producto(idLote) ON DELETE CASCADE,
    movimiento_producto_id INTEGER,
    cantidad INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

try:
    db_engine = connection.settings_dict.get('ENGINE', '')
    is_postgres = 'postgresql' in db_engine
    
    CREATE_TABLES_SQL = CREATE_TABLES_SQL_POSTGRES if is_postgres else CREATE_TABLES_SQL_SQLITE
    
    with connection.cursor() as cursor:
        for statement in CREATE_TABLES_SQL.split(';'):
            if statement.strip():
                cursor.execute(statement)
    print("Tablas creadas exitosamente")
except Exception as e:
    print(f"Error al crear tablas: {e}")

#!/usr/bin/env python
import os
import django
from django.conf import settings
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

# SQL para crear todas las tablas
CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS categoria (
    "idCategoria" BIGSERIAL PRIMARY KEY,
    "nombreCategoria" VARCHAR(50) NOT NULL,
    "descripcion" TEXT,
    "imagen" VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS subcategoria (
    "idSubcategoria" BIGSERIAL PRIMARY KEY,
    "nombreSubcategoria" VARCHAR(50) NOT NULL,
    "descripcion" TEXT,
    "idCategoria" BIGINT REFERENCES categoria("idCategoria") ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS productos (
    "idProducto" BIGSERIAL PRIMARY KEY,
    "nombreProducto" VARCHAR(50) NOT NULL,
    "precio" NUMERIC(10, 2) NOT NULL,
    "stock" INTEGER DEFAULT 0,
    "descripcion" TEXT,
    "lote" VARCHAR(100),
    "cantidadDisponible" INTEGER DEFAULT 0,
    "fechaIngreso" TIMESTAMP,
    "fechaVencimiento" DATE,
    "idCategoria" BIGINT REFERENCES categoria("idCategoria") ON DELETE SET NULL,
    "idSubcategoria" BIGINT REFERENCES subcategoria("idSubcategoria") ON DELETE SET NULL,
    "imagen" VARCHAR(100),
    "precio_venta" NUMERIC(10, 2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP,
    is_superuser BOOLEAN DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clientes (
    "idCliente" BIGSERIAL PRIMARY KEY,
    "nombreCliente" VARCHAR(100) NOT NULL,
    "apellidoCliente" VARCHAR(100) NOT NULL,
    "emailCliente" VARCHAR(100) UNIQUE NOT NULL,
    "telefonoCliente" VARCHAR(20),
    "direccionCliente" TEXT,
    "ciudadCliente" VARCHAR(50),
    "departamentoCliente" VARCHAR(50),
    "codigoPostalCliente" VARCHAR(20),
    usuario_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pedidos (
    "idPedido" BIGSERIAL PRIMARY KEY,
    "fechaPedido" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "estado" VARCHAR(50) DEFAULT 'En Preparacion',
    "total" NUMERIC(10, 2) DEFAULT 0,
    "idCliente" BIGINT NOT NULL REFERENCES clientes("idCliente") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS detallepedido (
    "idDetallePedido" BIGSERIAL PRIMARY KEY,
    "cantidad" INTEGER NOT NULL,
    "precioUnitario" NUMERIC(10, 2) NOT NULL,
    "subtotal" NUMERIC(10, 2) NOT NULL,
    "margen_ganancia" NUMERIC(5, 2) DEFAULT 0,
    "idPedido" BIGINT NOT NULL REFERENCES pedidos("idPedido") ON DELETE CASCADE,
    "idProducto" BIGINT NOT NULL REFERENCES productos("idProducto") ON DELETE CASCADE
);
"""

try:
    with connection.cursor() as cursor:
        for statement in CREATE_TABLES_SQL.split(';'):
            if statement.strip():
                cursor.execute(statement)
    print("Tablas creadas exitosamente")
except Exception as e:
    print(f"Error al crear tablas: {e}")

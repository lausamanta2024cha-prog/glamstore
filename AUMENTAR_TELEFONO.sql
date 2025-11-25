-- Script SQL para aumentar el tamaño del campo telefono en la tabla repartidores
-- Ejecutar esto en phpMyAdmin o MySQL Workbench

USE glamstoredb;

-- Verificar el tamaño actual del campo
DESCRIBE repartidores;

-- Aumentar el tamaño del campo telefono de 11 a 20 caracteres
ALTER TABLE repartidores MODIFY COLUMN telefono VARCHAR(20) NULL;

-- Verificar que se cambió correctamente
DESCRIBE repartidores;

-- Script SQL para agregar la columna email a la tabla repartidores
-- Ejecutar esto en phpMyAdmin o MySQL Workbench

USE glamstoredb;

-- Verificar si la columna ya existe
SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'repartidores' 
AND COLUMN_NAME = 'email';

-- Si no existe, ejecutar:
ALTER TABLE repartidores ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL;

-- Verificar que se agregó correctamente
DESCRIBE repartidores;

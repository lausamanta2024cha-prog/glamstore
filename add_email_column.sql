-- Agregar columna email a la tabla repartidores
ALTER TABLE repartidores ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL;

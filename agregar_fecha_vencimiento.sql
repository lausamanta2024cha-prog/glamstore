-- Agregar columna fecha_vencimiento a la tabla pedidos
ALTER TABLE pedidos ADD COLUMN fechaVencimiento DATE NULL;

-- Crear índice para mejor rendimiento
CREATE INDEX idx_fecha_vencimiento ON pedidos(fechaVencimiento);

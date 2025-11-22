-- Script para agregar el campo estado_pago a la tabla pedidos
-- Ejecutar este script en la base de datos

-- Agregar la columna estado_pago
ALTER TABLE pedidos ADD COLUMN estado_pago VARCHAR(20) DEFAULT 'Pago Completo';

-- Actualizar los registros existentes basándose en el estado actual
-- Si el estado actual contiene información de pago, extraerla
UPDATE pedidos 
SET estado_pago = 'Pago Parcial' 
WHERE estado LIKE '%Pago Parcial%' OR estado = 'Pago Parcial';

UPDATE pedidos 
SET estado_pago = 'Pago Completo' 
WHERE estado_pago IS NULL OR estado_pago = '';

-- Limpiar los estados que tenían información de pago mezclada
UPDATE pedidos 
SET estado = 'En Camino' 
WHERE estado = 'En Camino - Pago Parcial';

-- Verificar los cambios
SELECT idPedido, estado, estado_pago, total 
FROM pedidos 
ORDER BY idPedido DESC 
LIMIT 10;
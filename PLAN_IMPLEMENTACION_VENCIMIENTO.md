# 📋 PLAN DE IMPLEMENTACIÓN: SISTEMA DE VENCIMIENTO Y PDF MENSUAL

## 🎯 Objetivo
Implementar un sistema donde:
1. Cada pedido tiene fecha de vencimiento según ciudad
2. Se envía PDF mensual con TODOS los pedidos pendientes
3. Al completar entrega, se pregunta al cliente si recibió

## 📊 Lógica de Vencimiento

### Cálculo de Fecha de Vencimiento
- **Bogotá**: 2 días hábiles desde fecha del pedido
- **Soacha**: 3 días hábiles desde fecha del pedido

### Ejemplo
**Pedido #65** (24/11/2025 - Bogotá):
- Fecha pedido: 24/11/2025 (lunes)
- Día 1: 25/11/2025 (martes) ✓
- Día 2: 26/11/2025 (miércoles) ✓
- **Fecha vencimiento: 26/11/2025**

**Pedido #53** (24/11/2025 - Soacha):
- Fecha pedido: 24/11/2025 (lunes)
- Día 1: 25/11/2025 (martes) ✓
- Día 2: 26/11/2025 (miércoles) ✓
- Día 3: 27/11/2025 (jueves) ✓
- **Fecha vencimiento: 27/11/2025**

## 📅 PDF MENSUAL

### Contenido
- **Período**: Mes completo (ej: Noviembre 2025)
- **Repartidor**: Nombre del repartidor
- **Tabla con TODOS los pedidos pendientes**:
  - Número de pedido
  - Cliente
  - Teléfono
  - Dirección
  - Fecha pedido
  - Fecha vencimiento
  - Estado pago
  - Total
  - Estado actual

### Ejemplo de Tabla
| Pedido | Cliente | Teléfono | Dirección | Fecha Pedido | Vencimiento | Pago | Total | Estado |
|--------|---------|----------|-----------|--------------|-------------|------|-------|--------|
| #53 | michael | 3001234 | Soacha | 24/11/2025 | 27/11/2025 | ✓ | $93300 | En Camino |
| #54 | michael | 3001234 | Soacha | 24/11/2025 | 27/11/2025 | ✓ | $44510 | En Camino |
| #65 | alejandro | 3025464 | Bogotá | 24/11/2025 | 26/11/2025 | ⚠ | $77350 | En Camino |

## 🔄 Flujo de Estados

### Estados Actuales
1. **Confirmado** → Pedido confirmado, esperando repartidor
2. **En Camino** → Repartidor tiene el pedido
3. **Entregado** → Pedido entregado (estado actual)
4. **Completado** → NUEVO - Pedido entregado y cliente confirmó recepción

### Nuevo Flujo
```
Confirmado → En Camino → Entregado → Completado
                                        ↓
                            ¿Recibiste tu pedido?
                            Sí / No / Problema
```

## 📧 Cambios en el Correo/PDF

### Información Adicional a Incluir
1. **Fecha de vencimiento** para cada pedido
2. **Días restantes** para entregar
3. **Alerta si vence pronto** (rojo si vence en 1 día)

### Ejemplo de Alerta
```
Pedido #65 - VENCE HOY (26/11/2025)
Pedido #53 - Vence en 2 días (27/11/2025)
```

## 🛠️ Cambios Técnicos Necesarios

### 1. Modelo Pedido
Agregar campo:
```python
fecha_vencimiento = models.DateField(null=True, blank=True)
```

### 2. Función de Cálculo
```python
def calcular_fecha_vencimiento(fecha_pedido, ciudad):
    dias_vencimiento = 2 if 'bogota' in ciudad.lower() else 3
    fecha_actual = fecha_pedido
    dias_contados = 0
    
    while dias_contados < dias_vencimiento:
        fecha_actual += timedelta(days=1)
        if es_dia_habil(fecha_actual):  # Lunes a viernes
            dias_contados += 1
    
    return fecha_actual
```

### 3. Servicio de Correo
Actualizar `enviar_correo_repartidor_detallado()` para:
- Incluir fecha de vencimiento en tabla
- Mostrar días restantes
- Resaltar pedidos que vencen pronto

### 4. Vista de Confirmación
Nueva vista para cuando estado = "Entregado":
- Mostrar formulario: "¿Recibiste tu pedido?"
- Opciones: Sí / No / Problema
- Si "Sí" → cambiar a "Completado"
- Si "No" o "Problema" → crear notificación

## 📋 Pedidos Pendientes por Repartidor

### Repartidor: Juan Pérez
- Pedido #53: $93300 (Soacha - Vence 27/11)
- Pedido #54: $44510 (Soacha - Vence 27/11)
- Pedido #55: $84970 (Soacha - Vence 27/11)
- Pedido #56: $71400 (Soacha - Vence 27/11)

### Repartidor: Carlos Martínez
- Pedido #57: $39270 (Soacha - Vence 27/11)
- Pedido #58: $42840 (Bogotá - Vence 26/11)
- Pedido #59: $124240 (Bogotá - Vence 26/11)
- Pedido #60: $61880 (Bogotá - Vence 26/11)

### Repartidor: Ana Torre
- Pedido #61: $240860 (Bogotá - Vence 26/11)
- Pedido #62: $40940 (Bogotá - Vence 26/11)
- Pedido #63: $48080 (Bogotá - Vence 26/11)
- Pedido #64: $173030 (Bogotá - Vence 26/11)

### Repartidor: Lauren
- Pedido #65: $77350 (Bogotá - Vence 26/11)

## ✅ Próximos Pasos

1. Agregar campo `fecha_vencimiento` al modelo Pedido
2. Crear función para calcular fecha de vencimiento
3. Actualizar correo/PDF para mostrar fecha de vencimiento
4. Crear vista para confirmación de recepción
5. Cambiar estado a "Completado" cuando cliente confirme

---
**Estado**: 📋 PLAN LISTO PARA IMPLEMENTAR  
**Fecha**: 25/11/2025
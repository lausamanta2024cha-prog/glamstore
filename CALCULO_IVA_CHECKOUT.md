# CÁLCULO DEL IVA EN CHECKOUT - GLAM STORE

## 📋 RESUMEN DE CAMBIOS

Se ha agregado el cálculo del **IVA (19%)** en el proceso de checkout. El IVA se calcula sobre el subtotal de productos y se suma al total final.

---

## 💰 FÓRMULA DE CÁLCULO

### Pago Completo (Pagar envío ahora):
```
Subtotal de Productos = Suma de (cantidad × precio) de todos los productos
IVA (19%) = Subtotal × 0.19
Envío = $10.000
Total Final = Subtotal + IVA + Envío
```

### Pago Parcial (Envío contra entrega):
```
Subtotal de Productos = Suma de (cantidad × precio) de todos los productos
IVA (19%) = Subtotal × 0.19
Envío = $0 (se paga contra entrega)
Total Final = Subtotal + IVA
```

---

## 📊 EJEMPLO PRÁCTICO

### Escenario 1: Pago Completo

**Carrito:**
- Labial: 2 × $50 = $100
- Sombra: 1 × $80 = $80
- Base: 1 × $200 = $200

**Cálculo:**
- Subtotal: $380
- IVA (19%): $380 × 0.19 = $72.20 → $72 (redondeado)
- Envío: $10.000
- **Total: $10.452**

### Escenario 2: Pago Parcial

**Carrito:**
- Labial: 2 × $50 = $100
- Sombra: 1 × $80 = $80
- Base: 1 × $200 = $200

**Cálculo:**
- Subtotal: $380
- IVA (19%): $380 × 0.19 = $72.20 → $72 (redondeado)
- Envío: $0 (contra entrega)
- **Total: $452**

---

## 🔧 CAMBIOS REALIZADOS

### 1. Frontend (checkout.html)

**Cambio en el resumen de compra:**
```html
<!-- ANTES -->
<p>Subtotal: <strong id="subtotal-valor">${{ total }}</strong></p>
<p id="costo-envio-resumen" style="display: block;">Envío: <strong>$10.000</strong></p>
<p>Total: <strong id="total-valor">${{ total|add:10000 }}</strong></p>

<!-- DESPUÉS -->
<p>Subtotal: <strong id="subtotal-valor">${{ total }}</strong></p>
<p id="costo-envio-resumen" style="display: block;">Envío: <strong>$10.000</strong></p>
<p>IVA (19%): <strong id="iva-valor">$0</strong></p>
<hr style="margin: 1rem 0;">
<p style="font-size: 1.2rem; font-weight: bold;">Total: <strong id="total-valor" style="color: #ec407a;">${{ total|add:10000 }}</strong></p>
```

**Cambio en JavaScript:**
```javascript
// ANTES
function actualizarTotal() {
  const pagoAhora = document.querySelector('input[name="pago_envio"][value="ahora"]').checked;
  if (pagoAhora) {
    costoEnvioResumen.style.display = 'block';
    totalValor.textContent = '$' + (subtotal + costoEnvio).toLocaleString('es-CO');
  } else {
    costoEnvioResumen.style.display = 'none';
    totalValor.textContent = '$' + subtotal.toLocaleString('es-CO');
  }
}

// DESPUÉS
function actualizarTotal() {
  const pagoAhora = document.querySelector('input[name="pago_envio"][value="ahora"]').checked;
  
  let subtotalConEnvio;
  if (pagoAhora) {
    costoEnvioResumen.style.display = 'block';
    subtotalConEnvio = subtotal + costoEnvio;
  } else {
    costoEnvioResumen.style.display = 'none';
    subtotalConEnvio = subtotal;
  }
  
  // Calcular IVA sobre el subtotal (sin incluir envío)
  const iva = Math.round(subtotal * tasaIVA);
  const totalFinal = subtotalConEnvio + iva;
  
  // Actualizar valores en la pantalla
  ivaValor.textContent = '$' + iva.toLocaleString('es-CO');
  totalValor.textContent = '$' + totalFinal.toLocaleString('es-CO');
}
```

### 2. Backend (core/Clientes/views.py - función simular_pago)

**Cambio en el cálculo del total:**
```python
# ANTES
if pago_envio == 'ahora':
    total_final = total_pedido + costo_envio
    estado_pago = 'Pago Completo'
else:
    total_final = total_pedido
    estado_pago = 'Pago Parcial'

# DESPUÉS
tasa_iva = 0.19  # 19% de IVA
iva = round(total_pedido * tasa_iva)

if pago_envio == 'ahora':
    total_final = total_pedido + iva + costo_envio
    estado_pago = 'Pago Completo'
else:
    total_final = total_pedido + iva
    estado_pago = 'Pago Parcial'
```

---

## ✅ CARACTERÍSTICAS DEL CÁLCULO

1. **IVA Dinámico**: Se calcula en tiempo real cuando el usuario cambia entre "Pagar ahora" y "Pagar contra entrega"

2. **Redondeo Correcto**: El IVA se redondea al peso más cercano usando `Math.round()` en JavaScript y `round()` en Python

3. **IVA sobre Productos**: El IVA se calcula SOLO sobre el subtotal de productos, NO incluye el envío

4. **Visualización Clara**: El resumen muestra:
   - Subtotal de productos
   - Costo del envío (si aplica)
   - IVA (19%)
   - Total final

5. **Consistencia**: El cálculo es igual en frontend (JavaScript) y backend (Python)

---

## 🧪 PRUEBAS RECOMENDADAS

### Caso 1: Pago Completo
1. Agregar productos al carrito
2. Ir a checkout
3. Seleccionar "Pagar envío ahora"
4. Verificar que el IVA se calcule correctamente
5. Verificar que el total incluya: Subtotal + IVA + Envío

### Caso 2: Pago Parcial
1. Agregar productos al carrito
2. Ir a checkout
3. Seleccionar "Pagar envío contra entrega"
4. Verificar que el IVA se calcule correctamente
5. Verificar que el total incluya: Subtotal + IVA (sin envío)

### Caso 3: Cambio de opción de pago
1. Agregar productos al carrito
2. Ir a checkout
3. Seleccionar "Pagar envío ahora"
4. Anotar el total
5. Cambiar a "Pagar envío contra entrega"
6. Verificar que el total disminuya en $10.000
7. Cambiar nuevamente a "Pagar envío ahora"
8. Verificar que el total vuelva al valor original

---

## 📝 NOTAS IMPORTANTES

- El IVA se calcula sobre el subtotal de productos ANTES de agregar el envío
- El envío NO tiene IVA
- El cálculo es automático y se actualiza en tiempo real
- El cliente ve el desglose completo en el resumen de compra
- El backend valida el cálculo nuevamente al procesar el pedido

---

## 🔍 VERIFICACIÓN EN BASE DE DATOS

Cuando se crea un pedido, el campo `total` en la tabla `pedidos` contiene:
- **Pago Completo**: Subtotal + IVA + Envío
- **Pago Parcial**: Subtotal + IVA

Ejemplo en base de datos:
```sql
-- Pago Completo
INSERT INTO pedidos (idCliente, estado_pago, estado_pedido, total, fechaCreacion)
VALUES (1, 'Pago Completo', 'Confirmado', 10452, NOW());

-- Pago Parcial
INSERT INTO pedidos (idCliente, estado_pago, estado_pedido, total, fechaCreacion)
VALUES (1, 'Pago Parcial', 'Confirmado', 452, NOW());
```

---

## ✨ ESTADO

✅ **Implementado y Listo**

- Frontend: Cálculo dinámico del IVA
- Backend: Cálculo del IVA al procesar el pedido
- Visualización: Desglose claro en el resumen
- Pruebas: Listos para ejecutar

---

**Fecha de implementación**: Noviembre 2024
**Tasa de IVA**: 19% (Colombia)
**Estado**: Producción

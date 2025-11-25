# ✅ PLAN MENSUAL DE ENTREGAS - ACTUALIZADO

## 📧 Cambios en el Correo

### Saludo Personalizado
**Antes:**
```
Hola [Repartidor],
A continuación encontrarás los detalles de tu ruta de entregas para hoy...
```

**Ahora:**
```
Hola [Repartidor],
Te enviamos el plan mensual de entregas para [Mes]. A continuación encontrarás todos los pedidos que debes entregar con la información completa de ubicación y estado de pago...
```

### Asunto del Correo
**Antes:** `Ruta de entregas - [Repartidor] - 24/11/2025`

**Ahora:** `Plan Mensual de Entregas - [Repartidor] - November de 2025`

## 📋 Tabla del Plan Mensual

### Columnas Incluidas (11 columnas)
1. **Pedido** - Número del pedido (#65, #53, etc.)
2. **Cliente** - Nombre completo del cliente
3. **Teléfono** - Número de contacto
4. **Dirección** - Dirección completa que el cliente seleccionó
5. **Ciudad** - Bogotá o Soacha (extraído automáticamente)
6. **Comuna** - Comuna/localidad (extraído de la dirección)
7. **Pago** - ✓ Pagado o ⚠ Pago Parcial
8. **¿Cobrar?** - SÍ (si es pago parcial) o NO (si es pago completo)
9. **Total** - Monto del pedido en pesos
10. **Vencimiento** - Fecha de vencimiento (26/11, 27/11, etc.)
11. **Estado** - 🔴 VENCE HOY, ⚠️ Vence en X días, ❌ VENCIDO

### Ejemplo de Tabla

| Pedido | Cliente | Teléfono | Dirección | Ciudad | Comuna | Pago | ¿Cobrar? | Total | Vencimiento | Estado |
|--------|---------|----------|-----------|--------|--------|------|----------|-------|-------------|--------|
| #65 | alejandro rodriguez | 3025464 | calle123#4-5, Suba... | Bogotá | Suba | ⚠ Pago Parcial | SÍ | $77350 | 26/11/2025 | 🔴 VENCE HOY |
| #53 | michael | 3001234 | Soacha, Cundinamarca | Soacha | Cundinamarca | ✓ Pagado | NO | $93300 | 27/11/2025 | ⚠️ Vence en 2 días |
| #59 | alejandro rodriguez | 3025464 | Bogotá, Localidad... | Bogotá | Localidad | ✓ Pagado | NO | $124240 | 26/11/2025 | 🔴 VENCE HOY |

## 📄 PDF Mensual

### Título
**"Plan Mensual de Entregas"**

### Información del Encabezado
- Repartidor: [Nombre]
- Mes: [Mes y Año]

### Contenido
- Misma tabla que el correo
- Formato imprimible
- Fácil de llevar en ruta

## 🎯 Información Clave para el Repartidor

### 1. Ubicación Completa
- **Dirección**: Exactamente como el cliente la ingresó
- **Ciudad**: Bogotá o Soacha (para saber zona de entrega)
- **Comuna**: Localidad específica dentro de la ciudad

### 2. Estado de Pago
- **✓ Pagado**: Cliente pagó completo → NO cobrar envío
- **⚠ Pago Parcial**: Cliente pagó parcialmente → SÍ cobrar envío

### 3. Urgencia de Entrega
- **🔴 VENCE HOY**: Entregar hoy mismo
- **⚠️ Vence en X días**: Entregar dentro de X días
- **❌ VENCIDO**: Ya pasó la fecha de vencimiento

## 📊 Lógica de Vencimiento

### Cálculo Automático
- **Bogotá**: 2 días hábiles desde la fecha del pedido
- **Soacha**: 3 días hábiles desde la fecha del pedido
- Solo se cuentan lunes a viernes

### Ejemplo
- Pedido creado: 24/11/2025 (lunes)
- Ciudad: Bogotá
- Vencimiento: 26/11/2025 (miércoles) = 2 días hábiles

## ✅ Beneficios para el Repartidor

1. **Información Completa**: Tiene toda la información que necesita en un solo documento
2. **Fácil Identificación**: Sabe exactamente dónde ir (ciudad, comuna, dirección)
3. **Claridad en Cobro**: Sabe si debe cobrar el envío o no
4. **Urgencia Visual**: Ve claramente qué pedidos son urgentes
5. **Planificación**: Puede planificar su ruta mensual

## 🔄 Flujo Completo

1. Admin selecciona repartidores
2. Presiona "Enviar Correos Seleccionados"
3. Repartidor recibe correo con:
   - Saludo personalizado
   - Plan mensual de entregas
   - PDF adjunto con toda la información
4. Repartidor revisa la tabla y planifica su ruta
5. Repartidor sabe exactamente:
   - Dónde ir (dirección, ciudad, comuna)
   - Cuánto cobrar (pago completo o parcial)
   - Cuándo entregar (fecha de vencimiento)

---
**Actualización completada**: 25/11/2025  
**Estado**: LISTO PARA PRUEBAS
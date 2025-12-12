# Instrucciones para Exportar Datos de Render

## Opción 1: Usar la Consola de Render (Recomendado)

1. Ve a tu servicio en Render: https://dashboard.render.com
2. Selecciona tu servicio "glamstore"
3. Ve a la pestaña "Shell"
4. Ejecuta el siguiente comando:

```bash
python manage.py export_data
```

Esto creará dos archivos:
- `repartidores_export.json` - Todos los repartidores
- `notificaciones_export.json` - Todas las notificaciones

## Opción 2: Ejecutar Script de Sincronización

En la consola de Render, ejecuta:

```bash
python sync_data.py
```

Este script:
1. Exporta los datos a JSON
2. Hace commit automático a GitHub
3. Hace push de los cambios

## Opción 3: Descargar Archivos Manualmente

1. Ejecuta el comando de exportación (Opción 1)
2. Ve a "Files" en Render
3. Descarga los archivos JSON
4. Súbelos a GitHub manualmente

## Después de Exportar

Los archivos JSON estarán disponibles en:
- `repartidores_export.json`
- `notificaciones_export.json`

Estos archivos contienen todos los datos de repartidores y notificaciones que existen en la BD de Render.

## Para Importar en Otra BD

Si necesitas importar estos datos en otra base de datos, ejecuta:

```bash
python manage.py import_data
```

Asegúrate de que los archivos `repartidores_export.json` y `notificaciones_export.json` estén en el directorio raíz del proyecto.

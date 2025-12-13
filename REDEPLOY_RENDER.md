# Redeploy en Render

## Problema
El deploy anterior falló porque buscaba `restore_data.py` que no existe.

## Solución
He actualizado el `build.sh` para usar el script correcto: `ejecutar_en_render.py`

## Pasos para hacer redeploy

### Opción 1: Desde el dashboard de Render (Recomendado)
1. Ve a https://dashboard.render.com
2. Selecciona el servicio "glamstore"
3. Haz clic en el botón "Manual Deploy" o "Redeploy"
4. Espera a que termine el deploy

### Opción 2: Desde la terminal (si tienes acceso SSH)
```bash
# Conéctate a Render
ssh render@srv-xxxxx

# Ve al directorio del proyecto
cd ~/project/src

# Ejecuta el script de restauración
python ejecutar_en_render.py glamstoredb.sql
```

## Qué hace el nuevo build.sh

1. **Ejecuta migraciones** - `python manage.py migrate`
2. **Inicializa la BD** - `python init_db.py` (crea usuarios básicos)
3. **Restaura datos** - `python ejecutar_en_render.py glamstoredb.sql`
   - Crea secuencias de auto-incremento
   - Inserta todos los datos del dump de MySQL
   - Verifica que se insertaron correctamente
4. **Recopila archivos estáticos** - `python manage.py collectstatic --noinput`

## Verificación

Después del deploy, verifica que todo funcionó:

```bash
python manage.py shell
```

```python
from core.models import Repartidor, Usuario, Cliente, Pedido

print(f"Repartidores: {Repartidor.objects.count()}")
print(f"Usuarios: {Usuario.objects.count()}")
print(f"Clientes: {Cliente.objects.count()}")
print(f"Pedidos: {Pedido.objects.count()}")

# Ver un repartidor
if Repartidor.objects.exists():
    r = Repartidor.objects.first()
    print(f"\nPrimer repartidor: {r.nombre} ({r.email})")
```

## Si algo falla

### Error: "Archivo 'glamstoredb.sql' no encontrado"
- Verifica que `glamstoredb.sql` esté en el repositorio
- Asegúrate de que está en la raíz del proyecto

### Error: "duplicate key value violates unique constraint"
- Significa que hay datos duplicados
- Limpia las tablas antes de restaurar:
  ```bash
  python manage.py shell
  ```
  ```python
  from django.db import connection
  cursor = connection.cursor()
  cursor.execute("TRUNCATE TABLE repartidores CASCADE;")
  cursor.execute("TRUNCATE TABLE usuarios CASCADE;")
  cursor.execute("TRUNCATE TABLE clientes CASCADE;")
  ```

### Error: "column does not exist"
- Verifica que el mapeo de columnas sea correcto
- Revisa `ejecutar_en_render.py` en la sección `COLUMN_MAPPINGS`

## Próximos pasos

1. Haz el redeploy en Render
2. Verifica que los datos se insertaron
3. Prueba el registro de clientes
4. Prueba el login
5. Verifica que los repartidores aparecen en el admin

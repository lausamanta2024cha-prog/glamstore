# Instrucciones para Agregar la Columna Email a Repartidores

Si recibiste el error: `(1054, "Unknown column 'repartidores.email' in 'field list'")`

Ejecuta el siguiente comando SQL en tu base de datos MySQL:

```sql
ALTER TABLE repartidores ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL;
```

## Pasos:

1. Abre tu cliente MySQL (phpMyAdmin, MySQL Workbench, etc.)
2. Selecciona la base de datos `glamstoredb`
3. Ejecuta el comando SQL anterior
4. Recarga la página en tu navegador

## Alternativa con línea de comandos:

```bash
mysql -u root -p glamstoredb < add_email_column.sql
```

O directamente:

```bash
mysql -u root glamstoredb -e "ALTER TABLE repartidores ADD COLUMN email VARCHAR(100) NULL DEFAULT NULL;"
```

Después de ejecutar el comando, la columna estará disponible y el error desaparecerá.

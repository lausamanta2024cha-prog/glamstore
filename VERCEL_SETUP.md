# Configuración de Vercel para Glam Store

## Variables de Entorno Requeridas

En el panel de Vercel, ve a **Settings → Environment Variables** y agrega estas variables:

### 1. CLAVE_SECRETA
- **Descripción**: Clave secreta de Django
- **Valor**: Genera una clave segura (mínimo 50 caracteres)
- **Ejemplo**: `django-insecure-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z`

### 2. DEPURAR
- **Descripción**: Modo debug (debe ser False en producción)
- **Valor**: `False`

### 3. ALLOWED_HOSTS
- **Descripción**: Dominios permitidos
- **Valor**: `tu-dominio.vercel.app` (reemplaza con tu dominio real)
- **Ejemplo**: `glamstore.vercel.app`

### 4. URL_DE_LA_BASE_DE_DATOS
- **Descripción**: URL de conexión a MySQL
- **Formato**: `mysql://usuario:contraseña@host:puerto/nombre_base_datos`
- **Ejemplo**: `mysql://root:micontraseña@db.example.com:3306/glamstoredb`

**Opciones para MySQL:**
- **PlanetScale** (recomendado): https://planetscale.com
- **AWS RDS**: https://aws.amazon.com/rds/
- **DigitalOcean Managed Databases**: https://www.digitalocean.com/products/managed-databases/
- **Heroku Postgres** (si usas PostgreSQL): https://www.heroku.com/postgres

### 5. EMAIL_HOST_PASSWORD
- **Descripción**: Contraseña de aplicación de Gmail
- **Pasos para obtenerla**:
  1. Ve a https://myaccount.google.com/security
  2. Habilita "Verificación en dos pasos"
  3. Ve a "Contraseñas de aplicación"
  4. Selecciona "Correo" y "Windows"
  5. Copia la contraseña generada
- **Valor**: La contraseña de 16 caracteres generada por Google

## Pasos para Desplegar

1. **Conecta tu repositorio a Vercel**
   - Ve a https://vercel.com
   - Click en "New Project"
   - Selecciona tu repositorio de GitHub

2. **Configura las variables de entorno**
   - En el panel de Vercel, ve a **Settings → Environment Variables**
   - Agrega todas las variables listadas arriba

3. **Despliega**
   - Click en "Deploy"
   - Vercel ejecutará automáticamente:
     - Instalación de dependencias
     - Migraciones de base de datos
     - Recolección de archivos estáticos

4. **Verifica el despliegue**
   - Ve a tu dominio en Vercel
   - Verifica que la aplicación esté funcionando

## Solución de Problemas

### Error: "No module named 'mysqlclient'"
- Asegúrate de que `mysqlclient` esté en `requirements.txt`

### Error: "Connection refused"
- Verifica que la URL de la base de datos sea correcta
- Asegúrate de que tu base de datos esté accesible desde Vercel

### Error: "ALLOWED_HOSTS"
- Verifica que tu dominio de Vercel esté en la variable `ALLOWED_HOSTS`

### Error: "Email not sent"
- Verifica que `EMAIL_HOST_PASSWORD` sea correcto
- Asegúrate de haber generado una contraseña de aplicación en Gmail

## Notas Importantes

- **CLAVE_SECRETA**: Debe ser única y segura. Nunca la compartas.
- **DEPURAR**: Siempre debe ser `False` en producción.
- **URL_DE_LA_BASE_DE_DATOS**: Asegúrate de que sea accesible desde Vercel.
- **EMAIL_HOST_PASSWORD**: Usa una contraseña de aplicación, no tu contraseña de Gmail.

## Dominio Personalizado

Para usar un dominio personalizado:
1. Ve a **Settings → Domains** en Vercel
2. Agrega tu dominio
3. Sigue las instrucciones para configurar los registros DNS
4. Actualiza `ALLOWED_HOSTS` con tu dominio personalizado

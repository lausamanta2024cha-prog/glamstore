from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.Clientes import views as cliente_views
tienda_view = cliente_views.tienda

urlpatterns = [
 path('admin/', admin.site.urls),
path('', tienda_view, name='tienda'),# Ruta principal ahora usa la vista correcta
 path('', include('core.Clientes.urls')), # Rutas de la app Clientes
 path('gestion/', include('core.Gestion_admin.urls')),  # ← esta línea es clave

]

# Servir archivos media en desarrollo y producción
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
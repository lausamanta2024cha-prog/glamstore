import os
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile

class MediaFilesMiddleware:
    """Middleware para servir archivos media desde la base de datos o filesystem"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Si la URL comienza con /media/, intentar servir el archivo
        if request.path.startswith('/media/'):
            file_path = request.path[7:]  # Remover '/media/'
            
            # Primero intentar desde la base de datos
            try:
                from core.models.imagenes import ImagenProducto, ImagenCategoria
                
                # Buscar en imágenes de productos
                if file_path.startswith('productos/'):
                    imagen = ImagenProducto.objects.filter(ruta=file_path).first()
                    if imagen:
                        return HttpResponse(imagen.contenido, content_type='image/jpeg')
                
                # Buscar en imágenes de categorías
                elif file_path.startswith('categorias/'):
                    imagen = ImagenCategoria.objects.filter(ruta=file_path).first()
                    if imagen:
                        return HttpResponse(imagen.contenido, content_type='image/jpeg')
            except Exception as e:
                pass
            
            # Si no está en la base de datos, intentar desde el filesystem
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            # Verificar que el archivo existe y está dentro de MEDIA_ROOT
            if os.path.exists(full_path) and os.path.isfile(full_path):
                try:
                    return FileResponse(open(full_path, 'rb'))
                except Exception:
                    pass
        
        return self.get_response(request)

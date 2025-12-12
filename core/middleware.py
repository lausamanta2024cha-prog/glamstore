import os
from django.http import FileResponse, HttpResponse
from django.conf import settings

class MediaFilesMiddleware:
    """Middleware para servir archivos media desde el filesystem"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Si la URL comienza con /media/, intentar servir el archivo desde filesystem
        if request.path.startswith('/media/'):
            file_path = request.path[7:]  # Remover '/media/'
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            # Verificar que el archivo existe y está dentro de MEDIA_ROOT
            try:
                if os.path.exists(full_path) and os.path.isfile(full_path):
                    return FileResponse(open(full_path, 'rb'))
            except Exception:
                pass
        
        return self.get_response(request)

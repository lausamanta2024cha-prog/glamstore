from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.models.imagenes import ImagenProducto, ImagenCategoria
from core.models.productos import Producto
from core.models.categoria import Categoria
import os


@login_required
def subir_imagen_producto(request):
    """Vista para subir imágenes de productos"""
    if request.method == 'POST':
        archivo = request.FILES.get('imagen')
        id_producto = request.POST.get('id_producto')
        ruta = request.POST.get('ruta')
        
        if not archivo or not id_producto or not ruta:
            return JsonResponse({'error': 'Faltan datos'}, status=400)
        
        try:
            # Leer el contenido del archivo
            contenido = archivo.read()
            
            # Guardar en la base de datos
            imagen, created = ImagenProducto.objects.get_or_create(
                idProducto=int(id_producto),
                ruta=ruta,
                defaults={
                    'nombreArchivo': archivo.name,
                    'contenido': contenido
                }
            )
            
            if not created:
                # Actualizar si ya existe
                imagen.contenido = contenido
                imagen.nombreArchivo = archivo.name
                imagen.save()
            
            # También guardar en el filesystem para respaldo
            media_path = os.path.join('media', ruta)
            os.makedirs(os.path.dirname(media_path), exist_ok=True)
            with open(media_path, 'wb') as f:
                f.write(contenido)
            
            return JsonResponse({
                'success': True,
                'mensaje': f'Imagen {archivo.name} subida correctamente',
                'ruta': ruta
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # GET - mostrar formulario
    productos = Producto.objects.all()
    return render(request, 'subir_imagen_producto.html', {'productos': productos})


@login_required
def subir_imagen_categoria(request):
    """Vista para subir imágenes de categorías"""
    if request.method == 'POST':
        archivo = request.FILES.get('imagen')
        id_categoria = request.POST.get('id_categoria')
        ruta = request.POST.get('ruta')
        
        if not archivo or not id_categoria or not ruta:
            return JsonResponse({'error': 'Faltan datos'}, status=400)
        
        try:
            # Leer el contenido del archivo
            contenido = archivo.read()
            
            # Guardar en la base de datos
            imagen, created = ImagenCategoria.objects.get_or_create(
                idCategoria=int(id_categoria),
                ruta=ruta,
                defaults={
                    'nombreArchivo': archivo.name,
                    'contenido': contenido
                }
            )
            
            if not created:
                # Actualizar si ya existe
                imagen.contenido = contenido
                imagen.nombreArchivo = archivo.name
                imagen.save()
            
            # También guardar en el filesystem para respaldo
            media_path = os.path.join('media', ruta)
            os.makedirs(os.path.dirname(media_path), exist_ok=True)
            with open(media_path, 'wb') as f:
                f.write(contenido)
            
            return JsonResponse({
                'success': True,
                'mensaje': f'Imagen {archivo.name} subida correctamente',
                'ruta': ruta
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # GET - mostrar formulario
    categorias = Categoria.objects.all()
    return render(request, 'subir_imagen_categoria.html', {'categorias': categorias})

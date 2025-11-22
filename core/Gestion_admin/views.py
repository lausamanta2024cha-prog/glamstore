from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.db.models import Sum
from core.models.distribuidores import Distribuidor
from core.models.clientes import Cliente
from core.models.pedidos import Pedido
from core.models import Categoria, Subcategoria, Producto, Usuario, MovimientoProducto
from core.models.pedidos import DetallePedido
from django.contrib.auth import logout
from django.urls import reverse
from core.models.repartidores import Repartidor
from django.template.loader import get_template
from django.db.models import Count
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.hashers import make_password
import openpyxl
from django.utils import timezone
from decimal import Decimal


def index(request):

    return render(request, 'index.html')  # o cualquier plantilla que tengas
# Dashboard principal
def dashboard_admin_view(request):
    from django.db.models import Q, F, Max
    from django.utils import timezone
    
    # Definir umbrales de tiempo
    ahora = timezone.now()
    una_semana_atras = ahora - timedelta(days=7)
    dos_semanas_atras = ahora - timedelta(days=14)
    
    # === ESTADÍSTICAS GENERALES ===
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()
    ventas_totales = Pedido.objects.aggregate(total=Sum('total'))['total'] or 0
    
    # === PRODUCTOS MÁS VENDIDOS ===
    productos_mas_vendidos = DetallePedido.objects.filter(
        idPedido__fechaCreacion__gte=una_semana_atras
    ).values(
        'idProducto__idProducto',
        'idProducto__nombreProducto',
        'idProducto__imagen'
    ).annotate(
        total_vendido=Sum('cantidad'),
        ultima_venta=Max('idPedido__fechaCreacion')
    ).order_by('-total_vendido')[:5]
    
    # Agregar información de productos para las imágenes
    productos_vendidos_completos = []
    for item in productos_mas_vendidos:
        try:
            producto = Producto.objects.get(idProducto=item['idProducto__idProducto'])
            productos_vendidos_completos.append({
                'idProducto': producto.idProducto,
                'nombreProducto': producto.nombreProducto,
                'imagen': producto.imagen,
                'total_vendido': item['total_vendido'],
                'ultima_venta': item['ultima_venta'],
                'precio': producto.precio,
                'stock': producto.stock
            })
        except Producto.DoesNotExist:
            continue
    
    # === PRODUCTOS POR SURTIR ===
    productos_por_surtir = Producto.objects.filter(stock__lt=10).order_by('stock')[:10]
    
    # === ESTADÍSTICAS DE CLIENTES ===
    # Simulamos fechas de registro usando el ID (los más recientes tienen ID mayor)
    clientes_esta_semana = Cliente.objects.filter(
        idCliente__gte=Cliente.objects.aggregate(max_id=Max('idCliente'))['max_id'] - 10
    ).count() if Cliente.objects.exists() else 0
    
    clientes_semana_pasada = max(0, Cliente.objects.count() - clientes_esta_semana - 5)
    
    # === PEDIDOS NUEVOS ===
    pedidos_nuevos = Pedido.objects.filter(
        fechaCreacion__gte=una_semana_atras
    ).select_related('idCliente').order_by('-fechaCreacion')[:10]
    
    # === VENTAS POR CATEGORÍA ===
    ventas_por_categoria = DetallePedido.objects.filter(
        idPedido__fechaCreacion__gte=una_semana_atras
    ).values(
        'idProducto__idCategoria__nombreCategoria'
    ).annotate(
        total=Sum(F('cantidad') * F('precio_unitario')),
        categoria=F('idProducto__idCategoria__nombreCategoria')
    ).order_by('-total')[:5]
    
    # Limpiar datos para el template
    ventas_categoria_limpio = []
    for item in ventas_por_categoria:
        if item['categoria']:
            ventas_categoria_limpio.append({
                'categoria': item['categoria'],
                'total': float(item['total'] or 0)
            })
    
    # === PRODUCTO MÁS VENDIDO INDIVIDUAL ===
    producto_mas_vendido = productos_mas_vendidos[0] if productos_mas_vendidos else None
    
    # === REABASTECIMIENTO RECIENTE ===
    reabastecimientos_recientes = MovimientoProducto.objects.filter(
        tipo_movimiento='AJUSTE_MANUAL_ENTRADA',
        fecha__gte=una_semana_atras
    ).select_related('producto').order_by('-fecha')[:10]
    
    # Procesar reabastecimientos para extraer proveedor de la descripción
    reabastecimientos_procesados = []
    for mov in reabastecimientos_recientes:
        proveedor = "Sin especificar"
        fuente = "Manual"
        
        if mov.descripcion:
            if "Proveedor:" in mov.descripcion:
                proveedor = mov.descripcion.split("Proveedor:")[-1].strip()
                fuente = "Excel"
            elif "Reabastecimiento desde Excel" in mov.descripcion:
                fuente = "Excel"
        
        reabastecimientos_procesados.append({
            'producto': mov.producto.nombreProducto,
            'cantidad': mov.cantidad,
            'costo_unitario': float(mov.costo_unitario),
            'valor_total': float(mov.costo_unitario * Decimal(mov.cantidad)),
            'proveedor': proveedor,
            'fuente': fuente,
            'fecha': mov.fecha
        })

    context = {
        # Estadísticas generales
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_pedidos': total_pedidos,
        'ventas_totales': float(ventas_totales),
        
        # Productos
        'productos_mas_vendidos': productos_vendidos_completos,
        'producto_mas_vendido': producto_mas_vendido,
        'productos_por_surtir': productos_por_surtir,
        
        # Clientes
        'clientes_esta_semana': clientes_esta_semana,
        'clientes_semana_pasada': clientes_semana_pasada,
        
        # Pedidos
        'pedidos_nuevos': pedidos_nuevos,
        
        # Ventas por categoría
        'ventas_por_categoria': ventas_categoria_limpio,
        
        # Reabastecimiento reciente
        'reabastecimientos_recientes': reabastecimientos_procesados,
    }
    return render(request, 'admin_dashboard.html', context)
# core/views.py

# Panel Admin
def admin_productos_view(request):
    return render(request, 'admin_productos.html')

def lista_admin_view(request):
    # Fetch only users with id_rol = 1 (assuming 1 is the admin role)
    admins = Usuario.objects.filter(id_rol=1).order_by('nombre')
    return render(request, 'lista_admin.html', {'admins': admins})

def admin_agregar_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([nombre, email, password]):
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'admin_agregar.html', {'error': 'Todos los campos son obligatorios.'})

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Ya existe un usuario con este correo electrónico.")
            return render(request, 'admin_agregar.html', {'error': 'Ya existe un usuario con este correo electrónico.'})

        try:
            from django.utils import timezone
            nuevo_admin = Usuario.objects.create(
                nombre=nombre,
                email=email,
                password=make_password(password),
                id_rol=1,
                fechaCreacion=timezone.now()
            )
            return redirect('lista_admin')
        except Exception as e:
            print(f"Error al crear administrador: {str(e)}")
            messages.error(request, f"Error al crear el administrador: {str(e)}")
            return render(request, 'admin_agregar.html')

    return render(request, 'admin_agregar.html')


def admin_pedidos_view(request):
    return render(request, 'admin_pedidos.html')

def admin_usuarios_view(request):
    return render(request, 'admin_usuarios.html')

def admin_distribuidores_view(request):
    return render(request, 'admin_distribuidores.html')

def admin_repartidores_view(request):
    return render(request, 'admin_repartidores.html')

def admin_detalles_view(request):
    return render(request, 'admin_detalles.html')

def admin_eliminar_view(request, id):
    admin_to_delete = get_object_or_404(Usuario, idUsuario=id, id_rol=1)
    
    if request.session.get('usuario_id') == admin_to_delete.idUsuario:
        messages.error(request, "No puedes eliminar tu propia cuenta de administrador.")
        return redirect('lista_admin')

    if request.method == 'POST':
        admin_to_delete.delete()
        messages.success(request, "Administrador eliminado exitosamente.")
    return redirect('lista_admin')

# Panel Cliente



def lista_clientes_view(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return render(request, 'lista_clientes.html', context)




def cliente_editar_view(request, id):
    cliente = get_object_or_404(Cliente, idCliente=id)  # usa tu campo real

    if request.method == "POST":
        cliente.cedula = request.POST.get("cedula")
        cliente.nombre = request.POST.get("nombre")
        cliente.email = request.POST.get("email")
        cliente.direccion = request.POST.get("direccion")
        cliente.telefono = request.POST.get("telefono")
        cliente.save()
        return redirect("lista_clientes")  # vuelve al listado

    return render(request, "cliente_editar.html", {"cliente": cliente})


def cliente_eliminar_view(request, id):
    cliente = get_object_or_404(Cliente, idCliente=id)
    
    try:
        with transaction.atomic():
            # Primero, actualizar los usuarios relacionados para evitar el error de integridad referencial
            # Establecer idCliente a NULL para todos los usuarios que referencian este cliente
            usuarios_actualizados = Usuario.objects.filter(idCliente=id).update(idCliente=None)
            
            # Verificar si hay pedidos asociados al cliente
            pedidos_count = Pedido.objects.filter(idCliente=id).count()
            
            if pedidos_count > 0:
                messages.warning(request, f"El cliente {cliente.nombre} tiene {pedidos_count} pedido(s) asociado(s). Se eliminarán junto con el cliente.")
            
            # Ahora podemos eliminar el cliente de forma segura
            # Los pedidos se eliminarán automáticamente por la restricción de la base de datos
            cliente.delete()
            
            mensaje = f"Cliente {cliente.nombre} eliminado correctamente."
            if usuarios_actualizados > 0:
                mensaje += f" Se desvincularon {usuarios_actualizados} usuario(s) asociado(s)."
            
            messages.success(request, mensaje)
            
    except Exception as e:
        messages.error(request, f"Error al eliminar el cliente: {str(e)}")
    
    return redirect("lista_clientes")


# Panel Distribuidores
  # Asegúrate de que el modelo esté bien importado

def lista_distribuidores_view(request):
    distribuidores = Distribuidor.objects.all()
    return render(request, 'lista_distribuidores.html', {
        'distribuidores': distribuidores
    })


def distribuidor_agregar_view(request):
    if request.method == "POST":
        nombre = request.POST.get("nombreDistribuidor")
        contacto = request.POST.get("contacto")
 
        if nombre and contacto:
            Distribuidor.objects.create(
                nombreDistribuidor=nombre,
                contacto=contacto
            )
            return redirect("lista_distribuidores")
 
    return render(request, 'agregar_distribuidor.html')

def distribuidor_editar_view(request, id):
    distribuidor = get_object_or_404(Distribuidor, idDistribuidor=id)
    if request.method == "POST":
        distribuidor.nombreDistribuidor = request.POST.get("nombreDistribuidor")
        distribuidor.contacto = request.POST.get("contacto")
        distribuidor.save()
        return redirect("lista_distribuidores")
    return render(request, "distribuidor_editar.html", {"distribuidor": distribuidor})


def distribuidor_eliminar_view(request, id):
    distribuidor = get_object_or_404(Distribuidor, idDistribuidor=id)
    distribuidor.delete()
    return redirect("lista_distribuidores")

# Panel Productos
def lista_productos_view(request):
    productos = Producto.objects.all().order_by('nombreProducto')
    categorias = Categoria.objects.all()

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(idCategoria_id=categoria_id)

    # La ruta de la plantilla se corrige aquí
    return render(request, 'lista_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada_id': int(categoria_id) if categoria_id else None
    })

def producto_agregar_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreProducto')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        id_categoria = request.POST.get('idCategoria')
        id_subcategoria = request.POST.get('idSubcategoria')
        imagen = request.FILES.get('imagen')

        categoria = get_object_or_404(Categoria, idCategoria=id_categoria)
        subcategoria = None
        if id_subcategoria:
            subcategoria = get_object_or_404(Subcategoria, idSubcategoria=id_subcategoria)

        nuevo_producto = Producto.objects.create(
            nombreProducto=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=0,
            idCategoria=categoria,
            idSubcategoria=subcategoria,
            imagen=imagen
        )
        
        return redirect('lista_productos')

    categorias = Categoria.objects.prefetch_related('subcategoria_set').all()
    return render(request, 'productos_agregar.html', {
        'categorias': categorias
    })

def producto_editar_view(request, id):
    producto = get_object_or_404(Producto, idProducto=id)

    if request.method == 'POST':
        producto.nombreProducto = request.POST.get('nombreProducto')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        
        # El stock no se edita aquí, solo en movimientos_producto
        
        producto.idCategoria = get_object_or_404(Categoria, idCategoria=request.POST.get('idCategoria'))
        
        id_subcategoria = request.POST.get('idSubcategoria')
        producto.idSubcategoria = get_object_or_404(Subcategoria, idSubcategoria=id_subcategoria) if id_subcategoria else None

        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']
        
        producto.save()
        return redirect('lista_productos')

    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()
    return render(request, 'productos_editar.html', {'producto': producto, 'categorias': categorias, 'subcategorias': subcategorias})

def producto_eliminar_view(request, id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, idProducto=id)
        producto.delete()
    return redirect('lista_productos')

def movimientos_producto_view(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    movimientos = producto.movimientos.all().select_related('id_pedido')
    return render(request, 'movimientos_producto.html', {
        'producto': producto,
        'movimientos': movimientos
    })

def ajustar_stock_view(request, id):
    if request.method != 'POST':
        return redirect('movimientos_producto', id=id)

    producto = get_object_or_404(Producto, idProducto=id)
    
    try:
        cantidad = int(request.POST.get('cantidad'))
        tipo_ajuste = request.POST.get('tipo_ajuste')
        costo_unitario = request.POST.get('costo_unitario', 0)
        descripcion = request.POST.get('descripcion', 'Ajuste manual')

        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser un número positivo.")
            return redirect('movimientos_producto', id=id)

        stock_anterior = producto.stock
        diferencia = cantidad if tipo_ajuste == 'entrada' else -cantidad
        stock_nuevo = stock_anterior + diferencia

        tipo_movimiento = 'AJUSTE_MANUAL_ENTRADA' if tipo_ajuste == 'entrada' else 'AJUSTE_MANUAL_SALIDA'

        costo_a_registrar = 0
        if tipo_ajuste == 'entrada':
            costo_a_registrar = float(costo_unitario) if costo_unitario else 0

        MovimientoProducto.objects.create(
            producto=producto, tipo_movimiento=tipo_movimiento, cantidad=cantidad,
            stock_anterior=stock_anterior, stock_nuevo=stock_nuevo, descripcion=descripcion,
            costo_unitario=costo_a_registrar, precio_unitario=producto.precio
        )
        producto.stock = stock_nuevo
        producto.save()
        messages.success(request, "El stock ha sido ajustado correctamente.")
    except (ValueError, TypeError):
        messages.error(request, "Por favor, introduce una cantidad válida.")
    
    return redirect('movimientos_producto', id=id)

# Panel Reabastecimiento
def reabastecimiento_view(request):
    """Vista para cargar reabastecimiento desde Excel"""
    categorias = Categoria.objects.all()
    proveedores = Distribuidor.objects.all()
    productos_reabastecidos = request.session.pop('productos_reabastecidos', [])
    errores = request.session.pop('errores_reabastecimiento', [])
    
    if request.method == 'POST':
        archivo_excel = request.FILES.get('archivo_excel')
        categoria_id = request.POST.get('categoria_id')
        proveedor_id = request.POST.get('proveedor_id')
        
        if not archivo_excel:
            messages.error(request, "Por favor selecciona un archivo Excel.")
            return render(request, 'reabastecimiento.html', {'categorias': categorias, 'proveedores': proveedores})
        
        if not categoria_id:
            messages.error(request, "Por favor selecciona una categoría.")
            return render(request, 'reabastecimiento.html', {'categorias': categorias, 'proveedores': proveedores})
        
        if not proveedor_id:
            messages.error(request, "Por favor selecciona un proveedor.")
            return render(request, 'reabastecimiento.html', {'categorias': categorias, 'proveedores': proveedores})
        
        try:
            categoria = get_object_or_404(Categoria, idCategoria=categoria_id)
            proveedor = get_object_or_404(Distribuidor, idDistribuidor=proveedor_id)
            
            # Cargar el archivo Excel
            wb = openpyxl.load_workbook(archivo_excel)
            ws = wb.active
            
            productos_procesados = []
            errores_lista = []
            
            # Iterar sobre las filas (comenzando desde la fila 2, asumiendo que la fila 1 es encabezado)
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    nombre_producto = row[0]
                    cantidad = row[1]
                    costo_unitario = row[2]
                    
                    # Validar que los datos no sean None
                    if not nombre_producto or cantidad is None or costo_unitario is None:
                        errores_lista.append(f"Fila {row_idx}: Datos incompletos")
                        continue
                    
                    # Convertir a tipos correctos
                    cantidad = int(cantidad)
                    costo_unitario = Decimal(str(costo_unitario))
                    
                    # Buscar el producto por nombre en la categoría
                    producto = Producto.objects.filter(
                        nombreProducto__iexact=nombre_producto,
                        idCategoria=categoria
                    ).first()
                    
                    if not producto:
                        errores_lista.append(f"Fila {row_idx}: Producto '{nombre_producto}' no encontrado en la categoría")
                        continue
                    
                    # Crear movimiento de entrada
                    stock_anterior = producto.stock
                    stock_nuevo = stock_anterior + cantidad
                    
                    MovimientoProducto.objects.create(
                        producto=producto,
                        tipo_movimiento='AJUSTE_MANUAL_ENTRADA',
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                        costo_unitario=costo_unitario,
                        stock_anterior=stock_anterior,
                        stock_nuevo=stock_nuevo,
                        descripcion=f'Reabastecimiento desde Excel - {categoria.nombreCategoria} - Proveedor: {proveedor.nombreDistribuidor}'
                    )
                    
                    # Actualizar stock del producto
                    producto.stock = stock_nuevo
                    producto.save()
                    
                    # Guardar información del producto reabastecido
                    productos_procesados.append({
                        'nombre': producto.nombreProducto,
                        'cantidad': cantidad,
                        'costo_unitario': float(costo_unitario),
                        'stock_anterior': stock_anterior,
                        'stock_nuevo': stock_nuevo,
                        'valor_total': float(costo_unitario * Decimal(cantidad))
                    })
                    
                except (ValueError, TypeError) as e:
                    errores_lista.append(f"Fila {row_idx}: Error en los datos - {str(e)}")
                except Exception as e:
                    errores_lista.append(f"Fila {row_idx}: {str(e)}")
            
            # Guardar en sesión para mostrar en la página
            request.session['productos_reabastecidos'] = productos_procesados
            request.session['errores_reabastecimiento'] = errores_lista
            
            if errores_lista:
                for error in errores_lista:
                    messages.warning(request, error)
            
            return redirect('reabastecimiento')
            
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {str(e)}")
            return render(request, 'reabastecimiento.html', {'categorias': categorias, 'proveedores': proveedores})
    
    return render(request, 'reabastecimiento.html', {
        'categorias': categorias,
        'proveedores': proveedores,
        'productos_reabastecidos': productos_reabastecidos,
        'errores': errores
    })

# Panel Pedidos


def lista_pedidos_view(request):
    pedidos = Pedido.objects.all().order_by('-fechaCreacion') # Asegúrate que 'fechaCreacion' exista en el modelo Pedido
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

def pedido_agregar_view(request):
    if request.method == 'POST':
        # Lógica para agregar un nuevo pedido
        return redirect('lista_pedidos')
    return render(request, 'pedidos_agregar.html')

def pedido_editar_view(request, id):
    pedido = get_object_or_404(Pedido, idPedido=id)
    repartidores_disponibles = Repartidor.objects.filter(estado_turno='Disponible')

    if request.method == 'POST':
        # Comprobar si se está asignando un repartidor
        if 'asignar_repartidor' in request.POST:
            repartidor_id = request.POST.get('repartidor_id')
            repartidor_a_asignar = get_object_or_404(Repartidor, idRepartidor=repartidor_id)
            pedido.idRepartidor = repartidor_a_asignar
            pedido.save()
            # Opcional: Cambiar estado del repartidor a "En Ruta"
            # repartidor_a_asignar.estado_turno = 'En Ruta'
            # repartidor_a_asignar.save()
        else: # Si no, se está actualizando el estado del pedido
            pedido.estado = request.POST.get('estado')
            pedido.save()
        return redirect('editar_pedido', id=id) # Recargar la misma página
    return render(request, 'pedidos_editar.html', {'pedido': pedido, 'repartidores': repartidores_disponibles})

def pedido_eliminar_view(request, id):
    pedido = get_object_or_404(Pedido, idPedido=id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('lista_pedidos')
    return render(request, 'pedidos_eliminar.html', {'pedido': pedido})


def pedido_detalle_view(request, id):
    pedido = get_object_or_404(Pedido, idPedido=id)
    detalles = DetallePedido.objects.filter(idPedido=id)
    
    # Calcular total de unidades
    total_unidades = sum(detalle.cantidad for detalle in detalles)
    
    return render(request, 'pedidos_detalle.html', {
        'pedido': pedido,
        'detalles': detalles,
        'total_unidades': total_unidades
    })

def producto_detalle_view(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    
    # Obtener movimientos recientes del producto
    movimientos_recientes = MovimientoProducto.objects.filter(
        producto=id
    ).order_by('-fecha')[:5]
    
    # Calcular estadísticas del producto
    total_entradas = MovimientoProducto.objects.filter(
        producto=id,
        tipo_movimiento__in=['ENTRADA_INICIAL', 'AJUSTE_MANUAL_ENTRADA']
    ).aggregate(total=Sum('cantidad'))['total'] or 0
    
    total_salidas = MovimientoProducto.objects.filter(
        producto=id,
        tipo_movimiento__in=['SALIDA_VENTA', 'AJUSTE_MANUAL_SALIDA']
    ).aggregate(total=Sum('cantidad'))['total'] or 0
    
    return render(request, 'productos_detalle.html', {
        'producto': producto,
        'movimientos_recientes': movimientos_recientes,
        'total_entradas': total_entradas,
        'total_salidas': total_salidas
    })

def cliente_detalle_view(request, id):
    cliente = get_object_or_404(Cliente, idCliente=id)
    
    # Obtener todos los pedidos del cliente
    pedidos = Pedido.objects.filter(idCliente=id).order_by('-fechaCreacion')
    
    # Calcular estadísticas del cliente
    total_pedidos = pedidos.count()
    total_gastado = pedidos.aggregate(total=Sum('total'))['total'] or 0
    
    # Pedidos por estado
    pedidos_completados = pedidos.filter(estado='Pago Completo').count()
    pedidos_pendientes = pedidos.filter(estado='Pago Parcial').count()
    pedidos_sin_pago = pedidos.filter(estado='Sin Pago').count()
    
    # Pedidos recientes (últimos 5)
    pedidos_recientes = pedidos[:5]
    
    # Promedio de gasto por pedido
    promedio_gasto = total_gastado / total_pedidos if total_pedidos > 0 else 0
    
    return render(request, 'cliente_detalle.html', {
        'cliente': cliente,
        'pedidos': pedidos,
        'pedidos_recientes': pedidos_recientes,
        'total_pedidos': total_pedidos,
        'total_gastado': total_gastado,
        'pedidos_completados': pedidos_completados,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_sin_pago': pedidos_sin_pago,
        'promedio_gasto': promedio_gasto
    })

def admin_detalle_view(request, id):
    admin = get_object_or_404(Usuario, idUsuario=id, id_rol=1)  # Solo administradores
    
    # Obtener información adicional del administrador
    fecha_registro = admin.fechaRegistro if hasattr(admin, 'fechaRegistro') else None
    ultimo_acceso = admin.ultimoAcceso if hasattr(admin, 'ultimoAcceso') else None
    
    return render(request, 'admin_detalle.html', {
        'admin': admin,
        'fecha_registro': fecha_registro,
        'ultimo_acceso': ultimo_acceso
    })

# Panel Repartidores
def calcular_fecha_entrega(pedido):
    """Calcula la fecha de entrega según la ciudad del cliente"""
    from datetime import timedelta
    
    direccion_cliente = pedido.idCliente.direccion or ""
    direccion_lower = direccion_cliente.lower()
    
    if 'soacha' in direccion_lower:
        dias_entrega = 3
    elif 'bogota' in direccion_lower or 'bogotá' in direccion_lower:
        dias_entrega = 2
    else:
        dias_entrega = 3
    
    return pedido.fechaCreacion + timedelta(days=dias_entrega)

def verificar_y_actualizar_pedidos_entregados():
    """Verifica y actualiza automáticamente los pedidos que deben marcarse como entregados"""
    from django.utils import timezone
    
    # Obtener pedidos en estado "En Camino"
    pedidos_en_camino = Pedido.objects.filter(estado='En Camino').select_related('idCliente')
    
    ahora = timezone.now()
    pedidos_actualizados = 0
    
    for pedido in pedidos_en_camino:
        fecha_entrega = calcular_fecha_entrega(pedido)
        
        # Si ya pasó la fecha de entrega, marcar como entregado
        if ahora >= fecha_entrega:
            pedido.estado = 'Entregado'
            pedido.save()
            pedidos_actualizados += 1
    
    return pedidos_actualizados

def lista_repartidores_view(request):
    # Verificar y actualizar pedidos automáticamente
    verificar_y_actualizar_pedidos_entregados()
    
    # Obtener repartidores con conteo de pedidos
    from django.db.models import Count
    repartidores = Repartidor.objects.annotate(
        pedidos_count=Count('pedido')
    ).order_by('nombreRepartidor')
    
    # Filtros
    filtro_repartidor = request.GET.get('repartidor')
    filtro_estado = request.GET.get('estado')
    
    # Pedidos pendientes
    pedidos_pendientes = Pedido.objects.filter(
        idRepartidor__isnull=True,
        estado__in=['Pago Completo', 'Pago Parcial']
    ).select_related('idCliente').order_by('fechaCreacion')
    
    # Pedidos asignados
    pedidos_asignados = Pedido.objects.filter(
        idRepartidor__isnull=False
    ).select_related('idCliente', 'idRepartidor').order_by('-fechaCreacion')
    
    # Aplicar filtros
    if filtro_repartidor:
        pedidos_asignados = pedidos_asignados.filter(idRepartidor__idRepartidor=filtro_repartidor)
    
    if filtro_estado == 'pendiente':
        pedidos_asignados = Pedido.objects.none()  # No mostrar asignados
    elif filtro_estado == 'asignado':
        pedidos_pendientes = Pedido.objects.none()  # No mostrar pendientes
    
    return render(request, 'lista_repartidores.html', {
        'repartidores': repartidores,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_asignados': pedidos_asignados,
    })

def repartidor_agregar_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreRepartidor')
        telefono = request.POST.get('telefono')
        estado = request.POST.get('estado_turno')
        
        # Validación básica
        if not nombre or not telefono or not estado:
            # Puedes añadir un mensaje de error aquí
            return render(request, 'repartidores_agregar.html', {'error_message': 'Todos los campos son obligatorios.'})

        Repartidor.objects.create(
            nombreRepartidor=nombre,
            telefono=telefono,
            estado_turno=estado
        )
        return redirect('lista_repartidores')
    return render(request, 'repartidores_agregar.html')

def repartidor_editar_view(request, id):
    repartidor = get_object_or_404(Repartidor, idRepartidor=id)
    if request.method == 'POST':
        repartidor.nombreRepartidor = request.POST.get('nombreRepartidor')
        repartidor.telefono = request.POST.get('telefono')
        repartidor.estado_turno = request.POST.get('estado_turno')
        
        # Validación básica
        if not repartidor.nombreRepartidor or not repartidor.telefono or not repartidor.estado_turno:
            return render(request, 'repartidores_editar.html', {'repartidor': repartidor, 'error_message': 'Todos los campos son obligatorios.'})
        repartidor.save()
        return redirect('lista_repartidores')
    return render(request, 'repartidores_editar.html', {'repartidor': repartidor})

def repartidor_eliminar_view(request, id):
    if request.method == 'POST':
        repartidor = get_object_or_404(Repartidor, idRepartidor=id)
        repartidor.delete()
    return redirect('lista_repartidores')

def asignar_pedido_repartidor_view(request):
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        repartidor_id = request.POST.get('repartidor_id')

        pedido = get_object_or_404(Pedido.objects.select_related('idCliente'), idPedido=pedido_id)
        repartidor = get_object_or_404(Repartidor, idRepartidor=repartidor_id)

        # PRESERVAR el estado de pago original
        estado_original = pedido.estado
        
        # Asignar el repartidor al pedido
        pedido.idRepartidor = repartidor
        
        # Cambiar el estado del pedido preservando la información de pago
        if estado_original == 'Pago Parcial':
            # Era pago parcial, NO cambiar el estado para preservar la información
            pass  # Mantener 'Pago Parcial'
        elif estado_original == 'Pago Completo':
            # Era pago completo, cambiar a En Camino
            pedido.estado = 'En Camino'
        else:
            # Para cualquier otro estado, cambiar a En Camino
            pedido.estado = 'En Camino'
        
        pedido.save()

        # Cambiar el estado del repartidor a "En Ruta"
        repartidor.estado_turno = 'En Ruta'
        repartidor.save()

        # Redirigir a la lista de repartidores sin descargar PDF
        # El PDF se puede descargar usando el botón "Descargar PDF"
        return redirect('lista_repartidores')
    
    return redirect('lista_repartidores')

def generar_pdf_asignacion(request, pedido, repartidor, fecha_entrega, ciudad_entrega, dias_entrega):
    """Genera un PDF con los detalles de la asignación del pedido al repartidor"""
    detalles = DetallePedido.objects.filter(idPedido=pedido.idPedido).select_related('idProducto')
    
    context = {
        'pedido': pedido,
        'repartidor': repartidor,
        'detalles': detalles,
        'fecha_entrega': fecha_entrega,
        'ciudad_entrega': ciudad_entrega,
        'dias_entrega': dias_entrega,
    }
    
    template_path = 'asignacion_pedido_pdf.html'
    template = get_template(template_path)
    html = template.render(context)
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="asignacion_pedido_{pedido.idPedido}.pdf"'
        return response
    
    return HttpResponse('Ocurrió un error al generar el PDF.', status=500)

def desasignar_repartidor_view(request, id_pedido):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, idPedido=id_pedido)
        pedido.idRepartidor = None
        # Cambiar el estado de vuelta a su estado anterior
        if pedido.estado == 'En Camino':
            pedido.estado = 'Pago Completo'  # O el estado que corresponda
        pedido.save()
        # messages.success(request, f"Se ha desasignado el repartidor del pedido #{id_pedido}.")
    return redirect('lista_repartidores')

def descargar_pdf_asignacion_view(request, id_pedido):
    """Descarga el PDF de asignación de un pedido ya asignado"""
    pedido = get_object_or_404(Pedido.objects.select_related('idCliente', 'idRepartidor'), idPedido=id_pedido)
    
    # Verificar que el pedido tenga un repartidor asignado
    if not pedido.idRepartidor:
        return HttpResponse('Este pedido no tiene un repartidor asignado.', status=400)
    
    repartidor = pedido.idRepartidor
    
    # Calcular fecha de entrega según la ciudad
    direccion_cliente = pedido.idCliente.direccion or ""
    nombre_cliente = pedido.idCliente.nombre or ""
    email_cliente = pedido.idCliente.email or ""
    
    # Buscar en dirección, nombre y email del cliente
    texto_completo = f"{direccion_cliente} {nombre_cliente} {email_cliente}".lower()
    
    if 'soacha' in texto_completo:
        dias_entrega = 3
        ciudad_entrega = 'Soacha'
    elif 'bogota' in texto_completo or 'bogotá' in texto_completo:
        dias_entrega = 2
        ciudad_entrega = 'Bogotá'
    elif 'madrid' in texto_completo:
        dias_entrega = 3
        ciudad_entrega = 'Madrid'
    elif 'funza' in texto_completo:
        dias_entrega = 3
        ciudad_entrega = 'Funza'
    elif 'mosquera' in texto_completo:
        dias_entrega = 3
        ciudad_entrega = 'Mosquera'
    else:
        # Si no se puede determinar, usar Bogotá como predeterminado
        dias_entrega = 2
        ciudad_entrega = 'Bogotá (Predeterminado)'
    
    from datetime import timedelta
    fecha_entrega = pedido.fechaCreacion + timedelta(days=dias_entrega)
    
    # Generar el PDF
    return generar_pdf_asignacion(request, pedido, repartidor, fecha_entrega, ciudad_entrega, dias_entrega)

def descargar_pedido_pdf_view(request, id_pedido):
    pedido = get_object_or_404(Pedido.objects.select_related('idCliente', 'idRepartidor'), idPedido=id_pedido)
    detalles = DetallePedido.objects.filter(idPedido=id_pedido).select_related('idProducto')

    # Nota: El campo 'quien recibe' no se está guardando en el modelo Pedido actualmente.
    # Para incluirlo, se debería añadir un campo al modelo Pedido y guardarlo durante el checkout.

    context = {
        'pedido': pedido,
        'detalles': detalles,
    }

    template_path = 'pedido_pdf_template.html'
    template = get_template(template_path)
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Ocurrió un error al generar el PDF.', status=500)

# Panel Detalles
def lista_detalles_view(request):   
    return render(request, 'lista_detalles.html')   




def logout_view(request):
    logout(request)                
    request.session.flush()       
    response = redirect('login')  
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# API para cargar subcategorías dinámicamente
def api_subcategorias_view(request, categoria_id):
    """Devuelve las subcategorías de una categoría en formato JSON"""
    try:
        subcategorias = Subcategoria.objects.filter(
            categoria_id=categoria_id
        ).values('idSubcategoria', 'nombreSubcategoria')
        
        data = [
            {'id': sub['idSubcategoria'], 'nombre': sub['nombreSubcategoria']}
            for sub in subcategorias
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Panel Categorías
def lista_categorias_view(request):
    categorias = Categoria.objects.annotate(num_productos=Count('producto')).order_by('nombreCategoria')
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def categoria_agregar_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreCategoria')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        
        Categoria.objects.create(
            nombreCategoria=nombre, 
            descripcion=descripcion,
            imagen=imagen
        )
        return redirect('lista_categorias')
    return render(request, 'categoria_form.html', {'action': 'Agregar'})

def categoria_editar_view(request, id):
    categoria = get_object_or_404(Categoria, idCategoria=id)
    if request.method == 'POST':
        categoria.nombreCategoria = request.POST.get('nombreCategoria')
        categoria.descripcion = request.POST.get('descripcion')
        if 'imagen' in request.FILES:
            categoria.imagen = request.FILES['imagen']
        categoria.save()
        return redirect('lista_categorias')
    return render(request, 'categoria_form.html', {'form_object': categoria, 'action': 'Editar'})

def categoria_eliminar_view(request, id):
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, idCategoria=id)
        # Contar productos antes de eliminar
        if categoria.producto_set.count() > 0:
            print("No se puede eliminar: La categoría tiene productos asociados.") # Mensaje para depuración
        else:
            categoria.delete()
    return redirect('lista_categorias')

# Panel Subcategorías
def lista_subcategorias_view(request):
    subcategorias = Subcategoria.objects.all().select_related('categoria')
    return render(request, 'lista_subcategorias.html', {'subcategorias': subcategorias})

def subcategoria_agregar_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreSubcategoria')
        id_categoria = request.POST.get('idCategoria')
        
        if not nombre or not id_categoria:
            messages.error(request, "El nombre y la categoría son obligatorios.")
            categorias = Categoria.objects.all()
            return render(request, 'subcategoria_form.html', {'categorias': categorias, 'action': 'Agregar'})
        
        categoria_obj = get_object_or_404(Categoria, idCategoria=id_categoria)
        nueva_subcategoria = Subcategoria.objects.create(
            nombreSubcategoria=nombre, 
            categoria=categoria_obj
        )
        messages.success(request, f"Subcategoría '{nombre}' creada exitosamente.")
        return redirect('lista_subcategorias')
    categorias = Categoria.objects.all()
    return render(request, 'subcategoria_form.html', {'categorias': categorias, 'action': 'Agregar'})

def subcategoria_editar_view(request, id):
    subcategoria = get_object_or_404(Subcategoria, idSubcategoria=id)
    if request.method == 'POST':
        nombre = request.POST.get('nombreSubcategoria')
        id_categoria = request.POST.get('idCategoria')
        
        if not nombre or not id_categoria:
            messages.error(request, "El nombre y la categoría son obligatorios.")
            categorias = Categoria.objects.all()
            return render(request, 'subcategoria_form.html', {'form_object': subcategoria, 'categorias': categorias, 'action': 'Editar'})
        
        subcategoria.nombreSubcategoria = nombre
        subcategoria.categoria = get_object_or_404(Categoria, idCategoria=id_categoria)
        subcategoria.save()
        messages.success(request, f"Subcategoría '{nombre}' actualizada exitosamente.")
        return redirect('lista_subcategorias')
    categorias = Categoria.objects.all()
    return render(request, 'subcategoria_form.html', {'form_object': subcategoria, 'categorias': categorias, 'action': 'Editar'})

def subcategoria_eliminar_view(request, id):
    if request.method == 'POST':
        subcategoria = get_object_or_404(Subcategoria, idSubcategoria=id)
        nombre = subcategoria.nombreSubcategoria
        subcategoria.delete()
        messages.success(request, f"Subcategoría '{nombre}' eliminada exitosamente.")
    return redirect('lista_subcategorias')

def notificaciones_view(request):
    """Vista para mostrar las notificaciones de problemas de entrega"""
    from core.models import NotificacionProblema
    
    # Obtener todas las notificaciones ordenadas por fecha
    notificaciones = NotificacionProblema.objects.select_related(
        'idPedido__idCliente',
        'idPedido__idRepartidor'
    ).order_by('-fechaReporte')
    
    # Contar notificaciones no leídas
    notificaciones_no_leidas = notificaciones.filter(leida=False).count()
    
    return render(request, 'notificaciones.html', {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas
    })

def marcar_notificacion_leida(request, id_notificacion):
    """Marca una notificación como leída"""
    from core.models import NotificacionProblema
    
    if request.method == 'POST':
        notificacion = get_object_or_404(NotificacionProblema, idNotificacion=id_notificacion)
        notificacion.leida = True
        notificacion.save()
        messages.success(request, "Notificación marcada como leída.")
    
    return redirect('notificaciones')


def responder_notificacion_view(request, id_notificacion):
    """Vista para que el admin responda a una notificación de problema"""
    from core.models import NotificacionProblema
    from django.utils import timezone
    
    notificacion = get_object_or_404(NotificacionProblema, idNotificacion=id_notificacion)
    
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        
        if not respuesta:
            messages.error(request, "Por favor escribe una respuesta.")
            return render(request, 'responder_notificacion.html', {'notificacion': notificacion})
        
        notificacion.respuesta_admin = respuesta
        notificacion.fecha_respuesta = timezone.now()
        notificacion.save()
        
        messages.success(request, "Respuesta enviada al cliente.")
        return redirect('notificaciones')
    
    return render(request, 'responder_notificacion.html', {'notificacion': notificacion})


def asignar_pedidos_multiples_view(request):
    """Asigna múltiples pedidos a un repartidor de una vez"""
    if request.method == 'POST':
        pedido_ids = request.POST.getlist('pedido_ids')
        repartidor_id = request.POST.get('repartidor_id')
        
        if not pedido_ids or not repartidor_id:
            return redirect('lista_repartidores')
        
        repartidor = get_object_or_404(Repartidor, idRepartidor=repartidor_id)
        
        # Asignar todos los pedidos seleccionados
        pedidos_asignados = 0
        for pedido_id in pedido_ids:
            try:
                pedido = Pedido.objects.get(idPedido=pedido_id)
                pedido.idRepartidor = repartidor
                pedido.estado = 'En Camino'
                pedido.save()
                pedidos_asignados += 1
            except Pedido.DoesNotExist:
                continue
        
        # Cambiar el estado del repartidor a "En Ruta"
        if pedidos_asignados > 0:
            repartidor.estado_turno = 'En Ruta'
            repartidor.save()
        
        return redirect('lista_repartidores')
    
    return redirect('lista_repartidores')

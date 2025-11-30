
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
from .services_repartidores import (
    asignar_pedidos_automaticamente,
    enviar_pdf_repartidor,
    verificar_capacidad_repartidores,
    obtener_pedidos_sin_asignar,
    obtener_repartidores_disponibles
)


def index(request):

    return render(request, 'index.html')  # o cualquier plantilla que tengas
# Dashboard principal
def dashboard_admin_view(request):
    from django.db.models import Q, F, Max
    from django.utils import timezone
    
    # Asegurar que la columna email existe
    Repartidor.ensure_email_column_exists()
    
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
    # Calcular clientes únicos que hicieron pedidos esta semana y la semana pasada
    clientes_esta_semana = Pedido.objects.filter(
        fechaCreacion__gte=una_semana_atras
    ).values('idCliente').distinct().count()
    
    clientes_semana_pasada = Pedido.objects.filter(
        fechaCreacion__gte=dos_semanas_atras,
        fechaCreacion__lt=una_semana_atras
    ).values('idCliente').distinct().count()
    
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
    
    # Procesar reabastecimientos para extraer información de la descripción y campos directos
    reabastecimientos_procesados = []
    for mov in reabastecimientos_recientes:
        proveedor = "Sin especificar"
        fuente = "Manual"
        lote = mov.lote if mov.lote else None
        fecha_vencimiento = mov.fecha_vencimiento.strftime('%d/%m/%Y') if mov.fecha_vencimiento else None
        total_con_iva = int(mov.total_con_iva) if mov.total_con_iva is not None else None
        iva = int(mov.iva) if mov.iva is not None else None
        
        # Detectar si es Excel o Manual basándose en la descripción
        if mov.descripcion:
            if "Proveedor:" in mov.descripcion or "Reabastecimiento desde Excel" in mov.descripcion:
                fuente = "Excel"
                # Extraer información de la descripción para reabastecimientos desde Excel
                partes = mov.descripcion.split(" | ")
                for parte in partes:
                    if "Proveedor:" in parte:
                        proveedor = parte.split("Proveedor:")[-1].strip()
                    elif "Lote:" in parte and not lote:
                        lote = parte.split("Lote:")[-1].strip()
                    elif "Vencimiento:" in parte and not fecha_vencimiento:
                        fecha_str = parte.split("Vencimiento:")[-1].strip()
                        try:
                            if ' ' in fecha_str:
                                fecha_obj = datetime.strptime(fecha_str.split()[0], '%Y-%m-%d')
                                fecha_vencimiento = fecha_obj.strftime('%d/%m/%Y')
                            else:
                                fecha_vencimiento = fecha_str
                        except:
                            fecha_vencimiento = fecha_str
        
        # Calcular IVA y Total con IVA si no existen en la base de datos
        costo_unitario_val = int(mov.costo_unitario) if mov.costo_unitario else 0
        cantidad_val = mov.cantidad
        
        # Si no hay IVA guardado, calcularlo (19% del costo total)
        if iva is None and costo_unitario_val > 0 and cantidad_val > 0:
            costo_total = costo_unitario_val * cantidad_val
            iva = int(costo_total * Decimal('0.19'))
            total_con_iva = costo_total + iva
        
        reabastecimientos_procesados.append({
            'producto': mov.producto.nombreProducto,
            'cantidad': cantidad_val,
            'costo_unitario': costo_unitario_val,
            'valor_total': int(mov.costo_unitario * Decimal(mov.cantidad)) if mov.costo_unitario else 0,
            'proveedor': proveedor,
            'fuente': fuente,
            'lote': lote,
            'fecha_vencimiento': fecha_vencimiento,
            'total_con_iva': int(total_con_iva) if total_con_iva is not None else None,
            'iva': int(iva) if iva is not None else None,
            'stock_anterior': mov.stock_anterior,
            'stock_nuevo': mov.stock_nuevo,
            'fecha': mov.fecha
        })

    # === CALIFICACIONES DE REPARTIDORES ===
    from core.models import ConfirmacionEntrega
    from django.db.models import Avg, Count
    
    # Obtener calificaciones recientes (últimas 10)
    calificaciones_recientes = ConfirmacionEntrega.objects.select_related(
        'pedido', 'pedido__idCliente', 'repartidor'
    ).order_by('-fecha_confirmacion')[:10]
    
    # Repartidor estrella del mes (mejor promedio de calificación este mes)
    inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    repartidores_calificados = ConfirmacionEntrega.objects.filter(
        fecha_confirmacion__gte=inicio_mes,
        repartidor__isnull=False
    ).values(
        'repartidor__idRepartidor',
        'repartidor__nombreRepartidor',
        'repartidor__telefono'
    ).annotate(
        promedio_calificacion=Avg('calificacion'),
        total_entregas=Count('idConfirmacion')
    ).order_by('-promedio_calificacion', '-total_entregas')
    
    repartidor_estrella = repartidores_calificados.first() if repartidores_calificados.exists() else None

    # === NOTIFICACIONES NO LEÍDAS ===
    from core.models import NotificacionProblema
    
    # Solo contar problemas de entrega (los reportes se envían por correo)
    total_notificaciones_no_leidas = NotificacionProblema.objects.filter(leida=False).count()
    
    # === PEDIDOS SIN ASIGNAR REPARTIDOR ===
    # Incluir pedidos confirmados y en preparación sin repartidor
    pedidos_por_asignar = Pedido.objects.filter(
        idRepartidor__isnull=True
    ).exclude(
        estado_pedido__in=['Entregado', 'Completado', 'Cancelado']
    ).select_related('idCliente').order_by('-fechaCreacion')[:10]
    
    # Debug: imprimir información
    print(f"DEBUG - Pedidos sin repartidor encontrados: {pedidos_por_asignar.count()}")
    for p in pedidos_por_asignar:
        print(f"  Pedido #{p.idPedido} - Estado: {p.estado_pedido} - Cliente: {p.idCliente.nombre}")
    
    # === INFORMACIÓN DE VENCIMIENTOS ===
    from core.services.vencimientos_service import VencimientosService
    
    resumen_vencimientos = VencimientosService.obtener_resumen_vencimientos()
    productos_vencidos = resumen_vencimientos['productos_vencidos']
    productos_por_vencer = resumen_vencimientos['productos_por_vencer']
    
    context = {
        # Estadísticas generales
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_pedidos': total_pedidos,
        'ventas_totales': int(ventas_totales) if ventas_totales else 0,
        
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
        
        # Información de repartidores
        'hay_capacidad_repartidores': verificar_capacidad_repartidores(),
        'pedidos_sin_asignar': obtener_pedidos_sin_asignar().count(),
        'repartidores_disponibles': obtener_repartidores_disponibles().count(),
        
        # Calificaciones de repartidores
        'calificaciones_recientes': calificaciones_recientes,
        'repartidor_estrella': repartidor_estrella,
        
        # Notificaciones
        'total_notificaciones_no_leidas': total_notificaciones_no_leidas,
        
        # Pedidos por asignar
        'pedidos_por_asignar': pedidos_por_asignar,
        
        # Información de vencimientos
        'productos_vencidos': productos_vencidos,
        'productos_por_vencer': productos_por_vencer,
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
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Obtener todos los pedidos del cliente para eliminar registros relacionados
                pedidos = Pedido.objects.filter(idCliente=id)
                pedidos_count = pedidos.count()
                
                # Eliminar notificaciones de problemas relacionadas a los pedidos del cliente
                from core.models import NotificacionProblema
                notificaciones_eliminadas = 0
                for pedido in pedidos:
                    notificaciones = NotificacionProblema.objects.filter(idPedido=pedido)
                    notificaciones_eliminadas += notificaciones.count()
                    notificaciones.delete()
                
                # Eliminar detalles de pedidos (se eliminarán automáticamente por CASCADE)
                # Eliminar pedidos (se eliminarán automáticamente por CASCADE)
                
                # Actualizar los usuarios relacionados para evitar el error de integridad referencial
                usuarios_actualizados = Usuario.objects.filter(idCliente=id).update(idCliente=None)
                
                # Mostrar resumen de lo que se va a eliminar
                resumen = f"Se eliminaron: {pedidos_count} pedido(s)"
                if notificaciones_eliminadas > 0:
                    resumen += f", {notificaciones_eliminadas} notificación(es) de problema(s)"
                if usuarios_actualizados > 0:
                    resumen += f", {usuarios_actualizados} usuario(s) desvinculado(s)"
                
                # Ahora podemos eliminar el cliente de forma segura
                # Los pedidos y sus detalles se eliminarán automáticamente por la restricción CASCADE
                cliente.delete()
                
                mensaje = f"Cliente {cliente.nombre} y todos sus registros asociados han sido eliminados correctamente. {resumen}."
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
    
    # Productos con stock bajo (menos de 10 unidades)
    productos_stock_bajo = Producto.objects.filter(stock__lt=10).order_by('stock')

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(idCategoria_id=categoria_id)

    # La ruta de la plantilla se corrige aquí
    return render(request, 'lista_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada_id': int(categoria_id) if categoria_id else None,
        'productos_stock_bajo': productos_stock_bajo
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
    movimientos = producto.movimientos.all().select_related('id_pedido', 'lote_origen')
    
    # Obtener lotes disponibles para el producto
    from core.models import LoteProducto
    lotes_disponibles = LoteProducto.objects.filter(
        producto=producto,
        cantidad_disponible__gt=0
    ).order_by('fecha_entrada')
    
    # Obtener proveedores (distribuidores)
    proveedores = Distribuidor.objects.all().order_by('nombreDistribuidor')
    
    return render(request, 'movimientos_producto.html', {
        'producto': producto,
        'movimientos': movimientos,
        'lotes_disponibles': lotes_disponibles,
        'proveedores': proveedores
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
        lote = request.POST.get('lote', '')
        fecha_vencimiento = request.POST.get('fecha_vencimiento', '')
        iva = request.POST.get('iva', 0)
        total_con_iva = request.POST.get('total_con_iva', 0)
        lote_seleccionado_id = request.POST.get('lote_seleccionado')
        proveedor = request.POST.get('proveedor', '')

        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser un número positivo.")
            return redirect('movimientos_producto', id=id)

        stock_anterior = producto.stock
        diferencia = cantidad if tipo_ajuste == 'entrada' else -cantidad
        stock_nuevo = stock_anterior + diferencia

        tipo_movimiento = 'AJUSTE_MANUAL_ENTRADA' if tipo_ajuste == 'entrada' else 'AJUSTE_MANUAL_SALIDA'

        costo_a_registrar = 0
        iva_a_registrar = None
        total_con_iva_a_registrar = None
        fecha_venc_a_registrar = None
        lote_a_registrar = None

        if tipo_ajuste == 'entrada':
            # Convertir a entero (sin decimales) para pesos colombianos
            costo_a_registrar = int(float(costo_unitario)) if costo_unitario else 0
            # Limpiar valores de IVA y Total (remover puntos de separador de miles)
            if iva and str(iva).strip():
                iva_limpio = str(iva).replace('.', '').replace(',', '').strip()
                if iva_limpio and iva_limpio != '0':
                    iva_a_registrar = Decimal(iva_limpio)
            if total_con_iva and str(total_con_iva).strip():
                total_limpio = str(total_con_iva).replace('.', '').replace(',', '').strip()
                if total_limpio and total_limpio != '0':
                    total_con_iva_a_registrar = Decimal(total_limpio)
            lote_a_registrar = lote if lote else None
            fecha_venc_a_registrar = fecha_vencimiento if fecha_vencimiento else None

        from core.services import LotesService
        from core.models import LoteProducto
        
        if tipo_ajuste == 'entrada' and lote_a_registrar:
            # Usar el servicio de lotes para entradas con lote
            proveedor_a_registrar = proveedor if proveedor else None
            LotesService.crear_lote_entrada(
                producto=producto,
                codigo_lote=lote_a_registrar,
                cantidad=cantidad,
                costo_unitario=costo_a_registrar,
                fecha_vencimiento=fecha_venc_a_registrar,
                total_con_iva=total_con_iva_a_registrar,
                iva=iva_a_registrar,
                proveedor=proveedor_a_registrar,
                descripcion=descripcion
            )
        elif tipo_ajuste == 'salida' and lote_seleccionado_id:
            # Salida con lote específico seleccionado
            lote = get_object_or_404(LoteProducto, idLote=lote_seleccionado_id)
            
            if cantidad > lote.cantidad_disponible:
                messages.error(request, f"Solo hay {lote.cantidad_disponible} unidades disponibles en este lote.")
                return redirect('movimientos_producto', id=id)
            
            # Crear movimiento de salida
            MovimientoProducto.objects.create(
                producto=producto, 
                tipo_movimiento='AJUSTE_MANUAL_SALIDA', 
                cantidad=cantidad,
                stock_anterior=stock_anterior, 
                stock_nuevo=stock_nuevo, 
                descripcion=descripcion,
                costo_unitario=lote.costo_unitario, 
                precio_unitario=int(float(producto.precio)) if producto.precio else 0,
                lote=lote.codigo_lote,
                fecha_vencimiento=lote.fecha_vencimiento,
                lote_origen=lote
            )
            
            # Actualizar lote y producto
            lote.cantidad_disponible -= cantidad
            lote.save()
            producto.stock = stock_nuevo
            producto.save()
        else:
            # Lógica anterior para entradas sin lote
            MovimientoProducto.objects.create(
                producto=producto, 
                tipo_movimiento=tipo_movimiento, 
                cantidad=cantidad,
                stock_anterior=stock_anterior, 
                stock_nuevo=stock_nuevo, 
                descripcion=descripcion,
                costo_unitario=costo_a_registrar, 
                precio_unitario=int(float(producto.precio)) if producto.precio else 0,
                lote=lote_a_registrar,
                fecha_vencimiento=fecha_venc_a_registrar,
                iva=iva_a_registrar,
                total_con_iva=total_con_iva_a_registrar
            )
            producto.stock = stock_nuevo
            producto.save()
        messages.success(request, "El inventario ha sido ajustado correctamente.")
    except (ValueError, TypeError):
        messages.error(request, "Por favor, introduce una cantidad válida.")
    
    return redirect('movimientos_producto', id=id)

# Panel Reabastecimiento
def reabastecimiento_view(request):
    """Vista para cargar reabastecimiento desde Excel"""
    categorias = Categoria.objects.all()
    proveedores = Distribuidor.objects.all()
    productos_reabastecidos = request.session.get('productos_reabastecidos', [])
    errores = request.session.get('errores_reabastecimiento', [])
    
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
            
            # Cargar el archivo Excel (data_only=True para leer valores de fórmulas)
            wb = openpyxl.load_workbook(archivo_excel, data_only=True)
            ws = wb.active
            
            productos_procesados = []
            errores_lista = []
            
            # Iterar sobre las filas (comenzando desde la fila 2, asumiendo que la fila 1 es encabezado)
            # Columnas: Producto, Cantidad, Precio Unitario, Total con IVA, Lote, Fecha Vencimiento, IVA (19%)
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    nombre_producto = row[0]
                    cantidad = row[1]
                    precio_unitario = row[2]
                    total_con_iva = row[3]
                    lote = row[4] if len(row) > 4 else None
                    fecha_vencimiento = row[5] if len(row) > 5 else None
                    iva_valor = row[6] if len(row) > 6 else None
                    
                    # Validar que los datos básicos no sean None
                    if not nombre_producto or cantidad is None or precio_unitario is None:
                        errores_lista.append(f"Fila {row_idx}: Datos incompletos (Producto, Cantidad o Precio Unitario)")
                        continue
                    
                    # Convertir a tipos correctos
                    cantidad = int(cantidad)
                    precio_unitario = Decimal(str(precio_unitario))
                    
                    # Limpiar valores monetarios (remover $, puntos, comas)
                    if isinstance(total_con_iva, str):
                        total_con_iva = total_con_iva.replace('$', '').replace('.', '').replace(',', '').strip()
                    if total_con_iva and str(total_con_iva).strip():
                        try:
                            total_con_iva = Decimal(str(total_con_iva))
                        except:
                            total_con_iva = None
                    else:
                        total_con_iva = None
                    
                    if isinstance(iva_valor, str):
                        iva_valor = iva_valor.replace('$', '').replace('.', '').replace(',', '').strip()
                    if iva_valor and str(iva_valor).strip():
                        try:
                            iva_valor = Decimal(str(iva_valor))
                        except:
                            iva_valor = None
                    else:
                        iva_valor = None
                    
                    # Buscar el producto por nombre en la categoría
                    producto = Producto.objects.filter(
                        nombreProducto__iexact=nombre_producto,
                        idCategoria=categoria
                    ).first()
                    
                    if not producto:
                        errores_lista.append(f"Fila {row_idx}: Producto '{nombre_producto}' no encontrado en la categoría")
                        continue
                    
                    # Actualizar el precio del producto con el precio unitario del Excel
                    producto.precio = precio_unitario
                    
                    # Crear movimiento de entrada
                    stock_anterior = producto.stock
                    stock_nuevo = stock_anterior + cantidad
                    
                    # Construir descripción con toda la información
                    descripcion_partes = [
                        f'Reabastecimiento desde Excel - {categoria.nombreCategoria}',
                        f'Proveedor: {proveedor.nombreDistribuidor}'
                    ]
                    if lote:
                        descripcion_partes.append(f'Lote: {lote}')
                    if fecha_vencimiento:
                        descripcion_partes.append(f'Vencimiento: {fecha_vencimiento}')
                    if total_con_iva:
                        descripcion_partes.append(f'Total con IVA: ${total_con_iva:,.0f}')
                    if iva_valor:
                        descripcion_partes.append(f'IVA: ${iva_valor:,.0f}')
                    
                    descripcion_completa = ' | '.join(descripcion_partes)
                    
                    # Preparar valores para guardar
                    lote_a_guardar = lote if lote else None
                    fecha_venc_a_guardar = fecha_vencimiento if fecha_vencimiento else None
                    iva_a_guardar = Decimal(iva_valor) if iva_valor else None
                    total_iva_a_guardar = Decimal(total_con_iva) if total_con_iva else None
                    
                    MovimientoProducto.objects.create(
                        producto=producto,
                        tipo_movimiento='AJUSTE_MANUAL_ENTRADA',
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        costo_unitario=precio_unitario,
                        stock_anterior=stock_anterior,
                        stock_nuevo=stock_nuevo,
                        descripcion=descripcion_completa,
                        lote=lote_a_guardar,
                        fecha_vencimiento=fecha_venc_a_guardar,
                        iva=iva_a_guardar,
                        total_con_iva=total_iva_a_guardar
                    )
                    
                    # Actualizar stock y precio del producto
                    producto.stock = stock_nuevo
                    producto.save()
                    
                    # Convertir fecha a string si es datetime
                    fecha_venc_str = None
                    if fecha_vencimiento:
                        if isinstance(fecha_vencimiento, datetime):
                            fecha_venc_str = fecha_vencimiento.strftime('%d/%m/%Y')
                        else:
                            fecha_venc_str = str(fecha_vencimiento)
                    
                    # Guardar información del producto reabastecido
                    productos_procesados.append({
                        'nombre': producto.nombreProducto,
                        'cantidad': cantidad,
                        'costo_unitario': float(precio_unitario),
                        'stock_anterior': stock_anterior,
                        'stock_nuevo': stock_nuevo,
                        'valor_total': float(precio_unitario * Decimal(cantidad)),
                        'lote': str(lote) if lote else None,
                        'fecha_vencimiento': fecha_venc_str,
                        'total_con_iva': float(total_con_iva) if total_con_iva else None,
                        'iva': float(iva_valor) if iva_valor else None
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
    repartidores_disponibles = Repartidor.objects.all()

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            estado_pago = request.POST.get('estado_pago')
            estado_pedido = request.POST.get('estado_pedido')
            repartidor_id = request.POST.get('repartidor')
            total = request.POST.get('total')
            fecha_creacion = request.POST.get('fecha_creacion')
            
            # Actualizar total si se proporcionó
            if total:
                pedido.total = float(total)
            
            # Actualizar fecha si se proporcionó
            if fecha_creacion:
                from datetime import datetime
                pedido.fechaCreacion = datetime.fromisoformat(fecha_creacion.replace('T', ' '))
            
            # Actualizar estados de forma independiente
            if estado_pago:
                pedido.estado_pago = estado_pago
            
            if estado_pedido:
                # Validar el flujo de estados: Confirmado → En Preparación → En Camino → Entregado → Completado
                flujo_valido = {
                    'Confirmado': ['Confirmado', 'En Preparación', 'Problema en Entrega'],
                    'En Preparación': ['En Preparación', 'En Camino', 'Problema en Entrega'],
                    'En Camino': ['En Camino', 'Entregado', 'Problema en Entrega'],
                    'Entregado': ['Entregado', 'Completado', 'Problema en Entrega'],
                    'Completado': ['Completado'],
                    'Problema en Entrega': ['Problema en Entrega', 'Confirmado', 'En Preparación'],
                }
                
                estado_actual = pedido.estado_pedido
                if estado_actual not in flujo_valido or estado_pedido not in flujo_valido[estado_actual]:
                    messages.error(request, f"No se puede cambiar de '{estado_actual}' a '{estado_pedido}'. Flujo inválido.")
                    return redirect('editar_pedido', id=id)
                
                pedido.estado_pedido = estado_pedido
            
            # Asignar o desasignar repartidor
            if repartidor_id:
                repartidor = get_object_or_404(Repartidor, idRepartidor=repartidor_id)
                pedido.idRepartidor = repartidor
                # Cambiar estado del repartidor a "En Ruta" si se asigna
                repartidor.estado_turno = 'En Ruta'
                repartidor.save()
            else:
                # Si se desasigna el repartidor
                if pedido.idRepartidor:
                    repartidor_anterior = pedido.idRepartidor
                    repartidor_anterior.estado_turno = 'Disponible'
                    repartidor_anterior.save()
                pedido.idRepartidor = None
            
            pedido.save()
            
            messages.success(request, f"Pedido #{pedido.idPedido} actualizado correctamente.")
            return redirect('lista_pedidos')
            
        except Exception as e:
            messages.error(request, f"Error al actualizar el pedido: {str(e)}")
            return redirect('editar_pedido', id=id)
    
    return render(request, 'pedidos_editar.html', {
        'pedido': pedido, 
        'repartidores': repartidores_disponibles
    })

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
    
    # Pedidos por estado de pago
    pedidos_completados = pedidos.filter(estado_pago='Pago Completo').count()
    pedidos_pendientes = pedidos.filter(estado_pago='Pago Parcial').count()
    pedidos_sin_pago = pedidos.exclude(estado_pago__in=['Pago Completo', 'Pago Parcial']).count()
    
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
    pedidos_en_camino = Pedido.objects.filter(estado_pedido='En Camino').select_related('idCliente')
    
    ahora = timezone.now()
    pedidos_actualizados = 0
    
    for pedido in pedidos_en_camino:
        fecha_entrega = calcular_fecha_entrega(pedido)
        
        # Si ya pasó la fecha de entrega, marcar como entregado
        if ahora >= fecha_entrega:
            pedido.estado_pedido = 'Entregado'
            pedido.save()
            pedidos_actualizados += 1
    
    return pedidos_actualizados

def lista_repartidores_view(request):
    # Asegurar que la columna email existe
    Repartidor.ensure_email_column_exists()
    
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
    
    # Pedidos pendientes (sin repartidor asignado y con pago confirmado)
    pedidos_pendientes = Pedido.objects.filter(
        idRepartidor__isnull=True,
        estado_pago__in=['Pago Completo', 'Pago Parcial']
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
    # Asegurar que la columna telefono tiene el tamaño correcto
    Repartidor.ensure_telefono_column_size()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombreRepartidor')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        estado = request.POST.get('estado_turno')
        
        # Validación básica
        if not nombre or not telefono or not email or not estado:
            return render(request, 'repartidores_agregar.html', {'error_message': 'Todos los campos son obligatorios.'})

        Repartidor.objects.create(
            nombreRepartidor=nombre,
            telefono=telefono,
            email=email,
            estado_turno=estado
        )
        messages.success(request, f"Repartidor '{nombre}' agregado exitosamente.")
        return redirect('lista_repartidores')
    return render(request, 'repartidores_agregar.html')

def repartidor_editar_view(request, id):
    repartidor = get_object_or_404(Repartidor, idRepartidor=id)
    if request.method == 'POST':
        repartidor.nombreRepartidor = request.POST.get('nombreRepartidor')
        repartidor.telefono = request.POST.get('telefono')
        repartidor.email = request.POST.get('email')
        repartidor.estado_turno = request.POST.get('estado_turno')
        
        # Validación básica
        if not repartidor.nombreRepartidor or not repartidor.telefono or not repartidor.email or not repartidor.estado_turno:
            return render(request, 'repartidores_editar.html', {'repartidor': repartidor, 'error_message': 'Todos los campos son obligatorios.'})
        repartidor.save()
        messages.success(request, f"Repartidor '{repartidor.nombreRepartidor}' actualizado exitosamente.")
        return redirect('lista_repartidores')
    return render(request, 'repartidores_editar.html', {'repartidor': repartidor})

def repartidor_eliminar_view(request, id):
    if request.method == 'POST':
        repartidor = get_object_or_404(Repartidor, idRepartidor=id)
        repartidor.delete()
    return redirect('lista_repartidores')

def asignar_pedido_repartidor_view(request):
    from .services_repartidores import enviar_factura_cliente
    
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        repartidor_id = request.POST.get('repartidor_id')

        pedido = get_object_or_404(Pedido.objects.select_related('idCliente'), idPedido=pedido_id)
        repartidor = get_object_or_404(Repartidor, idRepartidor=repartidor_id)

        # Asignar el repartidor al pedido
        pedido.idRepartidor = repartidor
        
        # Cambiar el estado del pedido a "En Camino"
        pedido.estado_pedido = 'En Camino'
        
        pedido.save()

        # Cambiar el estado del repartidor a "En Ruta"
        repartidor.estado_turno = 'En Ruta'
        repartidor.save()
        
        # Enviar factura al cliente
        if enviar_factura_cliente(pedido):
            messages.success(request, f"Pedido #{pedido.idPedido} asignado. Factura enviada al cliente.")
        else:
            messages.warning(request, f"Pedido #{pedido.idPedido} asignado. No se pudo enviar la factura.")

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
        
        # Cambiar el estado del repartidor a disponible
        if pedido.idRepartidor:
            repartidor = pedido.idRepartidor
            repartidor.estado_turno = 'Disponible'
            repartidor.save()
        
        pedido.idRepartidor = None
        # Cambiar el estado del pedido de vuelta a Confirmado
        if pedido.estado_pedido == 'En Camino':
            pedido.estado_pedido = 'Confirmado'
        pedido.save()
        
        messages.success(request, f"Repartidor desasignado del pedido #{id_pedido}.")
    return redirect('lista_repartidores')

def desasignar_pedidos_multiples_view(request):
    if request.method == 'POST':
        pedido_ids = request.POST.getlist('pedido_ids_desasignar')
        
        if not pedido_ids:
            # Mensaje ocultado por solicitud del usuario
            return redirect('lista_repartidores')
        
        pedidos_desasignados = 0
        repartidores_liberados = set()
        
        for pedido_id in pedido_ids:
            try:
                pedido = Pedido.objects.get(idPedido=pedido_id)
                
                # Cambiar el estado del repartidor a disponible
                if pedido.idRepartidor:
                    repartidor = pedido.idRepartidor
                    repartidores_liberados.add(repartidor.nombreRepartidor)
                    repartidor.estado_turno = 'Disponible'
                    repartidor.save()
                
                # Desasignar repartidor
                pedido.idRepartidor = None
                
                # Cambiar el estado del pedido de vuelta a Confirmado
                if pedido.estado_pedido == 'En Camino':
                    pedido.estado_pedido = 'Confirmado'
                
                pedido.save()
                pedidos_desasignados += 1
                
            except Pedido.DoesNotExist:
                continue
        
        # Mensajes ocultados por solicitud del usuario
        pass
        
        return redirect('lista_repartidores')
    
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
    """Vista para mostrar las notificaciones de problemas de entrega y mensajes de contacto"""
    from core.models import NotificacionProblema, MensajeContacto
    
    # Obtener todas las notificaciones ordenadas por fecha
    notificaciones = NotificacionProblema.objects.select_related(
        'idPedido__idCliente',
        'idPedido__idRepartidor'
    ).order_by('-fechaReporte')
    
    # Contar notificaciones no leídas
    notificaciones_no_leidas = notificaciones.filter(leida=False).count()
    
    # Obtener mensajes de contacto ordenados por fecha
    mensajes_contacto = MensajeContacto.objects.all().order_by('-fecha')
    
    # Total de notificaciones no leídas (solo problemas de entrega)
    total_no_leidas = notificaciones_no_leidas
    
    return render(request, 'notificaciones.html', {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'mensajes_contacto': mensajes_contacto,
        'total_no_leidas': total_no_leidas
    })

def marcar_notificacion_leida(request, id_notificacion):
    """Marca una notificación como leída"""
    from core.models import NotificacionProblema
    
    if request.method == 'POST':
        notificacion = get_object_or_404(NotificacionProblema, idNotificacion=id_notificacion)
        notificacion.leida = True
        notificacion.save()
    
    return redirect('notificaciones')


def marcar_reporte_leido(request, id_reporte):
    """Marca un reporte como leído"""
    from core.models.notificaciones import NotificacionReporte
    
    if request.method == 'POST':
        reporte = get_object_or_404(NotificacionReporte, idNotificacion=id_reporte)
        reporte.leida = True
        reporte.save()
        messages.success(request, "Reporte marcado como leído.")
    
    return redirect('notificaciones')


def ver_reporte_view(request, id_reporte):
    """Vista para ver el contenido completo de un reporte"""
    from core.models.notificaciones import NotificacionReporte
    from django.http import HttpResponse
    
    reporte = get_object_or_404(NotificacionReporte, idNotificacion=id_reporte)
    
    # Marcar como leído automáticamente al verlo
    if not reporte.leida:
        reporte.leida = True
        reporte.save()
    
    # Devolver el HTML del reporte directamente
    return HttpResponse(reporte.contenido_html)


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
    from .services_repartidores import enviar_factura_cliente
    
    if request.method == 'POST':
        pedido_ids = request.POST.getlist('pedido_ids')
        repartidor_id = request.POST.get('repartidor_id')
        
        if not pedido_ids or not repartidor_id:
            return redirect('lista_repartidores')
        
        repartidor = get_object_or_404(Repartidor, idRepartidor=repartidor_id)
        
        # Asignar todos los pedidos seleccionados
        pedidos_asignados = 0
        facturas_enviadas = 0
        for pedido_id in pedido_ids:
            try:
                pedido = Pedido.objects.get(idPedido=pedido_id)
                pedido.idRepartidor = repartidor
                pedido.estado_pedido = 'En Camino'
                pedido.save()
                pedidos_asignados += 1
                
                # Enviar factura al cliente
                if enviar_factura_cliente(pedido):
                    facturas_enviadas += 1
                    
            except Pedido.DoesNotExist:
                continue
        
        # Cambiar el estado del repartidor a "En Ruta"
        if pedidos_asignados > 0:
            repartidor.estado_turno = 'En Ruta'
            repartidor.save()
        
        return redirect('lista_repartidores')
    
    return redirect('lista_repartidores')


# === GESTIÓN DE VENCIMIENTOS ===

def marcar_lotes_vencidos_view(request):
    """Vista para marcar lotes vencidos como perdidos"""
    if request.method == 'POST':
        from core.services.vencimientos_service import VencimientosService
        
        try:
            movimientos_creados = VencimientosService.marcar_lotes_vencidos_como_perdidos()
            # Redirigir sin mensaje
            return redirect('dashboard_admin')
        except Exception as e:
            # Redirigir sin mensaje de error
            return redirect('dashboard_admin')
    
    return redirect('dashboard_admin')


# === NUEVAS FUNCIONES PARA ASIGNACIÓN AUTOMÁTICA Y ENVÍO DE PDFs ===

def asignar_pedidos_automaticamente_view(request):
    """
    Vista para asignar automáticamente los pedidos a los repartidores disponibles
    Distribuye equitativamente entre todos los repartidores disponibles
    """
    if request.method == 'POST':
        try:
            # Asignar pedidos automáticamente (sin filtro de fecha)
            resultado = asignar_pedidos_automaticamente()
            
        except Exception as e:
            pass
    
    return redirect('lista_repartidores')


def enviar_pdfs_repartidores_view(request):
    """
    Vista para enviar correos detallados a todos los repartidores con pedidos asignados
    """
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        
        try:
            if fecha_str:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            else:
                fecha = timezone.now().date()
            
            # Obtener todos los repartidores con pedidos asignados para ese día
            repartidores_con_pedidos = Repartidor.objects.filter(
                pedido__estado_pedido__in=['En Camino', 'Confirmado'],
                pedido__fechaCreacion__date=fecha
            ).distinct()
            
            correos_enviados = 0
            errores = 0
            sin_email = 0
            
            for repartidor in repartidores_con_pedidos:
                # Verificar que tenga email
                if not repartidor.email:
                    sin_email += 1
                    continue
                
                # Intentar enviar correo detallado
                from .services_repartidores import enviar_correo_repartidor_detallado
                if enviar_correo_repartidor_detallado(repartidor, fecha):
                    correos_enviados += 1
                else:
                    errores += 1
            
            # Mensajes ocultados por solicitud del usuario
            pass
            
        except Exception as e:
            # Error silencioso - no mostrar al usuario
            pass
    
    return redirect('lista_repartidores')


def verificar_capacidad_repartidores_view(request):
    """
    Vista para verificar si hay suficientes repartidores para los pedidos del día
    """
    fecha_str = request.GET.get('fecha')
    
    try:
        if fecha_str:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        else:
            fecha = timezone.now().date()
        
        hay_capacidad = verificar_capacidad_repartidores(fecha)
        
        if hay_capacidad:
            return JsonResponse({
                'success': True,
                'mensaje': 'Hay suficientes repartidores para los pedidos del día.'
            })
        else:
            pedidos_sin_asignar = obtener_pedidos_sin_asignar(fecha).count()
            return JsonResponse({
                'success': False,
                'mensaje': f'No hay suficientes repartidores. Hay {pedidos_sin_asignar} pedidos sin asignar.'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error: {str(e)}'
        }, status=400)


def descargar_pdf_repartidor_view(request, repartidor_id):
    """
    Vista para descargar el PDF de pedidos de un repartidor específico
    """
    from .services_repartidores import generar_pdf_pedidos_repartidor
    
    repartidor = get_object_or_404(Repartidor, idRepartidor=repartidor_id)
    fecha_str = request.GET.get('fecha')
    
    try:
        if fecha_str:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        else:
            fecha = timezone.now().date()
        
        pdf_content = generar_pdf_pedidos_repartidor(repartidor, fecha)
        
        if pdf_content:
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="pedidos_{repartidor.idRepartidor}_{fecha.strftime("%Y%m%d")}.pdf"'
            return response
        else:
            messages.error(request, "No se pudo generar el PDF.")
            return redirect('lista_repartidores')
    
    except Exception as e:
        messages.error(request, f"Error al generar PDF: {str(e)}")
        return redirect('lista_repartidores')


def enviar_correos_repartidores_seleccionados_view(request):
    """
    Vista para enviar correos detallados a repartidores seleccionados
    """
    print(f"[DEBUG] Método de request: {request.method}")
    print(f"[DEBUG] Datos POST completos: {dict(request.POST)}")
    
    if request.method == 'POST':
        repartidor_ids = request.POST.getlist('repartidor_ids')
        print(f"[DEBUG] Repartidor IDs recibidos: {repartidor_ids}")
        print(f"[DEBUG] Tipo de repartidor_ids: {type(repartidor_ids)}")
        print(f"[DEBUG] Longitud de repartidor_ids: {len(repartidor_ids)}")
        
        if not repartidor_ids:
            print("[DEBUG] No se recibieron IDs de repartidores")
            # Mensaje ocultado por solicitud del usuario
            return redirect('lista_repartidores')
        
        try:
            fecha = timezone.now().date()
            correos_enviados = 0
            errores = 0
            sin_email = 0
            sin_pedidos = 0
            
            for repartidor_id in repartidor_ids:
                try:
                    repartidor = Repartidor.objects.get(idRepartidor=repartidor_id)
                    print(f"[DEBUG] Procesando repartidor: {repartidor.nombreRepartidor} (ID: {repartidor_id})")
                    
                    # Verificar que tenga email
                    if not repartidor.email:
                        print(f"[DEBUG] Repartidor sin email")
                        sin_email += 1
                        continue
                    
                    print(f"[DEBUG] Email: {repartidor.email}")
                    
                    # Verificar que tenga pedidos (SIN FILTRO DE FECHA - TODOS LOS PENDIENTES)
                    total_pedidos = Pedido.objects.filter(
                        idRepartidor=repartidor,
                        estado_pedido__in=['En Camino', 'Confirmado']
                    ).count()
                    
                    print(f"[DEBUG] Total de pedidos pendientes: {total_pedidos}")
                    
                    if total_pedidos == 0:
                        print(f"[DEBUG] Sin pedidos")
                        sin_pedidos += 1
                        continue
                    
                    # Intentar enviar correo detallado
                    print(f"[DEBUG] Enviando correo...")
                    from .services_repartidores import enviar_correo_repartidor_detallado
                    if enviar_correo_repartidor_detallado(repartidor, fecha):
                        print(f"[DEBUG] Correo enviado exitosamente")
                        correos_enviados += 1
                    else:
                        print(f"[DEBUG] Error al enviar correo")
                        errores += 1
                        
                except Repartidor.DoesNotExist:
                    print(f"[DEBUG] Repartidor no encontrado: {repartidor_id}")
                    errores += 1
                    continue
                except Exception as e:
                    print(f"[DEBUG] Excepción: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    errores += 1
                    continue
            
            # Mensajes ocultados por solicitud del usuario
            pass
            
            print(f"[DEBUG] Resumen: {correos_enviados} enviados, {sin_email} sin email, {sin_pedidos} sin pedidos, {errores} errores")
            
        except Exception as e:
            # Error silencioso - no mostrar al usuario
            pass
    
    return redirect('lista_repartidores')


def enviar_factura_cliente_view(request, id_pedido):
    """
    Vista para enviar la factura al cliente de un pedido específico
    """
    from .services_repartidores import enviar_factura_cliente
    
    if request.method == 'POST':
        try:
            pedido = get_object_or_404(Pedido.objects.select_related('idCliente', 'idRepartidor'), idPedido=id_pedido)
            
            if enviar_factura_cliente(pedido):
                messages.success(request, f"Factura enviada exitosamente a {pedido.idCliente.email}")
            else:
                if not pedido.idCliente.email:
                    messages.error(request, f"El cliente {pedido.idCliente.nombre} no tiene email registrado")
                else:
                    messages.error(request, "No se pudo enviar la factura. Intenta de nuevo.")
                    
        except Exception as e:
            messages.error(request, f"Error al enviar factura: {str(e)}")
    
    return redirect('lista_repartidores')


def enviar_facturas_multiples_view(request):
    """
    Vista para enviar facturas a múltiples clientes de una vez
    """
    from .services_repartidores import enviar_factura_cliente
    
    if request.method == 'POST':
        pedido_ids = request.POST.getlist('pedido_ids_facturas')
        
        if not pedido_ids:
            messages.warning(request, "Por favor selecciona al menos un pedido.")
            return redirect('lista_repartidores')
        
        try:
            facturas_enviadas = 0
            errores = 0
            
            for pedido_id in pedido_ids:
                try:
                    pedido = Pedido.objects.select_related('idCliente', 'idRepartidor').get(idPedido=pedido_id)
                    
                    if enviar_factura_cliente(pedido):
                        # Incrementar contador de facturas enviadas
                        pedido.facturas_enviadas += 1
                        pedido.save()
                        facturas_enviadas += 1
                    else:
                        errores += 1
                        
                except Pedido.DoesNotExist:
                    errores += 1
                    continue
                except Exception as e:
                    print(f"[DEBUG] Error al enviar factura del pedido {pedido_id}: {str(e)}")
                    errores += 1
                    continue
            
            # Mostrar resumen
            if facturas_enviadas > 0:
                messages.success(request, f"Se enviaron {facturas_enviadas} factura(s) exitosamente.")
            if errores > 0:
                messages.warning(request, f"Hubo {errores} error(es) al enviar facturas.")
                
        except Exception as e:
            messages.error(request, f"Error al enviar facturas: {str(e)}")
    
    return redirect('lista_repartidores')


def enviar_reporte_dashboard_view(request):
    """
    Vista para enviar un reporte completo del dashboard por correo electrónico
    con graficos de barras CSS y datos precisos
    """
    from django.core.mail import EmailMultiAlternatives
    from django.db.models import Q, F, Max, Avg, Count, Min
    from core.models import ConfirmacionEntrega
    from django.conf import settings
    
    if request.method != 'POST':
        return redirect('dashboard_admin')
    
    try:
        ahora = timezone.now()
        una_semana_atras = ahora - timedelta(days=7)
        dos_semanas_atras = ahora - timedelta(days=14)
        inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # === ESTADÍSTICAS GENERALES ===
        total_productos = Producto.objects.count()
        total_clientes = Cliente.objects.count()
        total_pedidos = Pedido.objects.count()
        ventas_totales = Pedido.objects.aggregate(total=Sum('total'))['total'] or 0
        
        # === CLIENTES NUEVOS (basado en primer pedido) ===
        # Clientes que hicieron su PRIMER pedido esta semana
        clientes_con_primer_pedido = Pedido.objects.values('idCliente').annotate(
            primer_pedido=Min('fechaCreacion')
        )
        clientes_nuevos_semana = sum(1 for c in clientes_con_primer_pedido if c['primer_pedido'] and c['primer_pedido'] >= una_semana_atras)
        clientes_nuevos_semana_pasada = sum(1 for c in clientes_con_primer_pedido if c['primer_pedido'] and dos_semanas_atras <= c['primer_pedido'] < una_semana_atras)
        
        # Clientes activos (que compraron) esta semana vs semana pasada
        clientes_activos_semana = Pedido.objects.filter(fechaCreacion__gte=una_semana_atras).values('idCliente').distinct().count()
        clientes_activos_semana_pasada = Pedido.objects.filter(fechaCreacion__gte=dos_semanas_atras, fechaCreacion__lt=una_semana_atras).values('idCliente').distinct().count()
        
        # === VENTAS POR CATEGORÍA ===
        ventas_por_categoria = DetallePedido.objects.values(
            'idProducto__idCategoria__nombreCategoria'
        ).annotate(
            total=Sum(F('cantidad') * F('precio_unitario')),
            cantidad_vendida=Sum('cantidad')
        ).order_by('-total')
        
        # === PRODUCTOS MÁS VENDIDOS ===
        productos_mas_vendidos = DetallePedido.objects.values(
            'idProducto__nombreProducto'
        ).annotate(
            total_vendido=Sum('cantidad'),
            ingresos=Sum(F('cantidad') * F('precio_unitario'))
        ).order_by('-total_vendido')[:10]
        
        # === PEDIDOS POR DÍA (últimos 7 días) ===
        pedidos_por_dia = []
        for i in range(6, -1, -1):
            dia = ahora - timedelta(days=i)
            inicio_dia = dia.replace(hour=0, minute=0, second=0, microsecond=0)
            fin_dia = dia.replace(hour=23, minute=59, second=59, microsecond=999999)
            count = Pedido.objects.filter(fechaCreacion__gte=inicio_dia, fechaCreacion__lte=fin_dia).count()
            ventas_dia = Pedido.objects.filter(fechaCreacion__gte=inicio_dia, fechaCreacion__lte=fin_dia).aggregate(total=Sum('total'))['total'] or 0
            dias_espanol = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
            dia_nombre = dias_espanol[dia.weekday()]
            pedidos_por_dia.append({
                'dia': f"{dia_nombre} {dia.day}",
                'pedidos': count,
                'ventas': float(ventas_dia)
            })
        
        # === PRODUCTOS CON INVENTARIO BAJO ===
        productos_bajo_stock = Producto.objects.filter(stock__lt=10).order_by('stock')
        
        # === REABASTECIMIENTOS RECIENTES ===
        reabastecimientos = MovimientoProducto.objects.filter(
            tipo_movimiento='AJUSTE_MANUAL_ENTRADA',
            fecha__gte=una_semana_atras
        ).select_related('producto').order_by('-fecha')[:15]
        
        # === PEDIDOS RECIENTES ===
        pedidos_recientes = Pedido.objects.select_related('idCliente').order_by('-fechaCreacion')[:15]
        
        # === REPARTIDOR ESTRELLA ===
        repartidores_calificados = ConfirmacionEntrega.objects.filter(
            fecha_confirmacion__gte=inicio_mes,
            repartidor__isnull=False
        ).values(
            'repartidor__nombreRepartidor',
            'repartidor__telefono'
        ).annotate(
            promedio=Avg('calificacion'),
            entregas=Count('idConfirmacion')
        ).order_by('-promedio', '-entregas')
        
        repartidor_estrella = repartidores_calificados.first()
        
        # === CALIFICACIONES Y ENTREGAS CONFIRMADAS ===
        total_entregas_confirmadas = ConfirmacionEntrega.objects.filter(
            fecha_confirmacion__gte=inicio_mes
        ).count()
        
        promedio_calificacion_general = ConfirmacionEntrega.objects.filter(
            fecha_confirmacion__gte=inicio_mes
        ).aggregate(promedio=Avg('calificacion'))['promedio'] or 0
        
        # === INFORMACIÓN DE VENCIMIENTOS ===
        from core.services.vencimientos_service import VencimientosService
        
        resumen_vencimientos = VencimientosService.obtener_resumen_vencimientos()
        productos_vencidos = resumen_vencimientos['productos_vencidos']
        productos_por_vencer = resumen_vencimientos['productos_por_vencer']
        
        # === CALCULAR TOTALES DE VENTAS ===
        ventas_semana = Pedido.objects.filter(
            fechaCreacion__gte=una_semana_atras
        ).aggregate(total=Sum('total'))['total'] or 0
        
        ventas_mes = Pedido.objects.filter(
            fechaCreacion__gte=inicio_mes
        ).aggregate(total=Sum('total'))['total'] or 0
        
        pedidos_semana = Pedido.objects.filter(fechaCreacion__gte=una_semana_atras).count()
        pedidos_mes = Pedido.objects.filter(fechaCreacion__gte=inicio_mes).count()
        
        # Calcular máximos para las barras
        max_ventas_cat = max([c['total'] or 0 for c in ventas_por_categoria]) if ventas_por_categoria else 1
        max_pedidos_dia = max([p['pedidos'] for p in pedidos_por_dia]) if pedidos_por_dia else 1
        max_ventas_dia = max([p['ventas'] for p in pedidos_por_dia]) if pedidos_por_dia else 1
        max_vendido = max([p['total_vendido'] for p in productos_mas_vendidos]) if productos_mas_vendidos else 1
        
        # === CONSTRUIR HTML DEL CORREO ===
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #fffafc; padding: 20px; }}
                .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
                h1 {{ color: #c2185b; border-bottom: 3px solid #f48fb1; padding-bottom: 10px; }}
                h2 {{ color: #ad1457; margin-top: 30px; margin-bottom: 15px; }}
                .stat-box {{ display: inline-block; background: #fce4ec; padding: 15px 25px; border-radius: 10px; margin: 8px; text-align: center; min-width: 120px; }}
                .stat-number {{ font-size: 1.8rem; font-weight: bold; color: #c2185b; }}
                .stat-label {{ color: #666; font-size: 0.85rem; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #fce4ec; }}
                th {{ background: #fce4ec; color: #c2185b; }}
                .highlight {{ background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #fbc02d; }}
                .footer {{ text-align: center; color: #999; margin-top: 30px; padding-top: 20px; border-top: 2px solid #fce4ec; }}
                .bar-container {{ margin: 8px 0; }}
                .bar-label {{ display: inline-block; width: 150px; font-size: 0.9rem; color: #333; }}
                .bar-wrapper {{ display: inline-block; width: calc(100% - 250px); background: #f5f5f5; border-radius: 5px; height: 25px; vertical-align: middle; }}
                .bar {{ height: 25px; border-radius: 5px; display: inline-block; }}
                .bar-value {{ display: inline-block; width: 80px; text-align: right; font-weight: bold; color: #c2185b; font-size: 0.9rem; }}
                .chart-vertical {{ display: flex; align-items: flex-end; justify-content: space-around; height: 200px; background: #fafafa; border-radius: 10px; padding: 20px 10px 10px 10px; margin: 15px 0; }}
                .chart-bar {{ display: flex; flex-direction: column; align-items: center; width: 12%; }}
                .chart-bar-fill {{ width: 100%; background: linear-gradient(180deg, #ec407a 0%, #f48fb1 100%); border-radius: 5px 5px 0 0; min-height: 5px; }}
                .chart-bar-label {{ font-size: 0.75rem; color: #666; margin-top: 8px; text-align: center; }}
                .chart-bar-value {{ font-size: 0.8rem; font-weight: bold; color: #c2185b; margin-bottom: 5px; }}
                .comparison-box {{ display: inline-block; background: white; padding: 15px 20px; border-radius: 10px; margin: 8px; border: 2px solid #f8bbd0; text-align: center; min-width: 180px; }}
                .comparison-title {{ font-size: 0.85rem; color: #666; margin-bottom: 5px; }}
                .comparison-value {{ font-size: 1.5rem; font-weight: bold; color: #c2185b; }}
                .comparison-change {{ font-size: 0.8rem; padding: 3px 8px; border-radius: 10px; margin-top: 5px; display: inline-block; }}
                .change-up {{ background: #e8f5e9; color: #2e7d32; }}
                .change-down {{ background: #ffebee; color: #c62828; }}
                .change-same {{ background: #f5f5f5; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Reporte Dashboard - Glam Store</h1>
                <p style="color: #666;">Generado el {ahora.strftime('%d/%m/%Y')} a las {ahora.strftime('%H:%M')}</p>
                
                <h2>Resumen General</h2>
                <div style="text-align: center;">
                    <div class="stat-box">
                        <div class="stat-number">{total_productos}</div>
                        <div class="stat-label">Productos</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{total_clientes}</div>
                        <div class="stat-label">Clientes</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{total_pedidos}</div>
                        <div class="stat-label">Pedidos Totales</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">${ventas_totales:,.0f}</div>
                        <div class="stat-label">Ventas Totales</div>
                    </div>
                </div>
                
                <h2>Comparativa Semanal</h2>
                <div style="text-align: center;">
                    <div class="comparison-box">
                        <div class="comparison-title">Clientes Nuevos Esta Semana</div>
                        <div class="comparison-value">{clientes_nuevos_semana}</div>
                        <div class="comparison-change {'change-up' if clientes_nuevos_semana > clientes_nuevos_semana_pasada else 'change-down' if clientes_nuevos_semana < clientes_nuevos_semana_pasada else 'change-same'}">
                            vs {clientes_nuevos_semana_pasada} semana pasada
                        </div>
                    </div>
                    <div class="comparison-box">
                        <div class="comparison-title">Clientes Activos Esta Semana</div>
                        <div class="comparison-value">{clientes_activos_semana}</div>
                        <div class="comparison-change {'change-up' if clientes_activos_semana > clientes_activos_semana_pasada else 'change-down' if clientes_activos_semana < clientes_activos_semana_pasada else 'change-same'}">
                            vs {clientes_activos_semana_pasada} semana pasada
                        </div>
                    </div>
                    <div class="comparison-box">
                        <div class="comparison-title">Pedidos Esta Semana</div>
                        <div class="comparison-value">{pedidos_semana}</div>
                        <div class="comparison-change">
                            ${ventas_semana:,.0f} en ventas
                        </div>
                    </div>
                    <div class="comparison-box">
                        <div class="comparison-title">Pedidos Este Mes</div>
                        <div class="comparison-value">{pedidos_mes}</div>
                        <div class="comparison-change">
                            ${ventas_mes:,.0f} en ventas
                        </div>
                    </div>
                </div>
                
                <h2>Pedidos por Dia (Ultimos 7 dias)</h2>
                <table>
                    <tr>
                        <th>Dia</th>
                        <th>Pedidos</th>
                        <th>Ventas</th>
                        <th>Grafico</th>
                    </tr>
        """
        
        for dia in pedidos_por_dia:
            porcentaje = int((dia['pedidos'] / max_pedidos_dia) * 100) if max_pedidos_dia > 0 else 0
            html_content += f"""
                    <tr>
                        <td style="font-weight: bold;">{dia['dia']}</td>
                        <td style="text-align: center;">{dia['pedidos']}</td>
                        <td style="text-align: right;">${dia['ventas']:,.0f}</td>
                        <td style="width: 40%;">
                            <div style="background: #f5f5f5; border-radius: 5px; height: 20px; width: 100%;">
                                <div style="background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%); height: 20px; width: {porcentaje}%; border-radius: 5px;"></div>
                            </div>
                        </td>
                    </tr>
            """
        
        html_content += """
                </table>
                
                <h2>Ventas por Categoria</h2>
        """
        
        for cat in ventas_por_categoria:
            if cat['idProducto__idCategoria__nombreCategoria']:
                porcentaje = int((cat['total'] or 0) / max_ventas_cat * 100) if max_ventas_cat > 0 else 0
                html_content += f"""
                <div class="bar-container">
                    <span class="bar-label">{cat['idProducto__idCategoria__nombreCategoria']}</span>
                    <span class="bar-wrapper">
                        <span class="bar" style="width: {porcentaje}%; background: linear-gradient(90deg, #ec407a 0%, #f48fb1 100%);"></span>
                    </span>
                    <span class="bar-value">${cat['total'] or 0:,.0f}</span>
                </div>
                """
        
        html_content += """
                
                <h2>Top 10 Productos Mas Vendidos</h2>
        """
        
        for i, prod in enumerate(productos_mas_vendidos, 1):
            porcentaje = int((prod['total_vendido'] / max_vendido) * 100) if max_vendido > 0 else 0
            colores = ['#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#00bcd4', '#009688', '#4caf50', '#8bc34a', '#cddc39']
            color = colores[(i-1) % len(colores)]
            html_content += f"""
                <div class="bar-container">
                    <span class="bar-label" style="width: 200px;">{i}. {prod['idProducto__nombreProducto'][:25]}</span>
                    <span class="bar-wrapper" style="width: calc(100% - 300px);">
                        <span class="bar" style="width: {porcentaje}%; background: {color};"></span>
                    </span>
                    <span class="bar-value">{prod['total_vendido']} uds</span>
                </div>
            """
        
        html_content += """
                
                <h2>Inventario Bajo (Stock menor a 10)</h2>
                <div style="background: #ffebee; padding: 15px; border-radius: 10px; border-left: 4px solid #f44336;">
        """
        
        for prod in productos_bajo_stock:
            porcentaje_stock = int((prod.stock / 10) * 100)
            color_barra = '#c62828' if prod.stock < 3 else '#f57c00' if prod.stock < 6 else '#fbc02d'
            html_content += f"""
                <div class="bar-container">
                    <span class="bar-label" style="width: 200px;">{prod.nombreProducto[:25]}</span>
                    <span class="bar-wrapper" style="width: calc(100% - 280px); background: #ffcdd2;">
                        <span class="bar" style="width: {porcentaje_stock}%; background: {color_barra};"></span>
                    </span>
                    <span class="bar-value" style="color: {color_barra};">{prod.stock} uds</span>
                </div>
            """
        
        html_content += "</div>"
        
        # === SECCIÓN DE VENCIMIENTOS ===
        html_content += """
                
                <h2>Control de Vencimientos</h2>
        """
        
        # Productos Vencidos
        html_content += f"""
                <div style="background: #ffebee; padding: 15px; border-radius: 10px; border-left: 4px solid #f44336; margin-bottom: 20px;">
                    <h3 style="color: #f44336; margin: 0 0 10px 0;">Productos Vencidos</h3>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                        <div><strong>Total productos:</strong> {productos_vencidos['total_productos']}</div>
                        <div><strong>Cantidad perdida:</strong> {productos_vencidos['total_cantidad']} unidades</div>
                        <div><strong>Valor perdido:</strong> ${productos_vencidos['total_valor']:,.0f}</div>
                    </div>
        """
        
        if productos_vencidos['total_productos'] > 0:
            html_content += """
                    <table style="width: 100%; margin-top: 10px;">
                        <tr style="background: #ffcdd2;">
                            <th>Producto</th><th>Lote</th><th>Días Vencido</th><th>Cantidad</th><th>Valor Perdido</th>
                        </tr>
            """
            for item in productos_vencidos['detalle']:
                html_content += f"""
                        <tr>
                            <td>{item['producto'].nombreProducto}</td>
                            <td>{item['lote'].codigo_lote}</td>
                            <td style="color: #f44336; font-weight: bold;">{item['dias_vencido']} días</td>
                            <td style="text-align: center;">{item['cantidad_perdida']}</td>
                            <td style="text-align: right;">${item['valor_perdido']:,.0f}</td>
                        </tr>
                """
            html_content += "</table>"
        else:
            html_content += '<p style="color: #4caf50; text-align: center; margin: 0;">No hay productos vencidos</p>'
        
        html_content += "</div>"
        
        # Productos por Vencer
        html_content += f"""
                <div style="background: #fff3e0; padding: 15px; border-radius: 10px; border-left: 4px solid #ff9800; margin-bottom: 20px;">
                    <h3 style="color: #ff9800; margin: 0 0 10px 0;">Productos por Vencer (30 días)</h3>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                        <div><strong>Total productos:</strong> {productos_por_vencer['total_productos']}</div>
                        <div><strong>Cantidad en riesgo:</strong> {productos_por_vencer['total_cantidad']} unidades</div>
                        <div><strong>Valor en riesgo:</strong> ${productos_por_vencer['total_valor']:,.0f}</div>
                    </div>
                    <div style="display: flex; gap: 20px; margin-bottom: 15px; font-size: 0.9rem;">
                        <span style="color: #f44336;"><strong>Críticos (≤7 días):</strong> {productos_por_vencer['criticos']}</span>
                        <span style="color: #ff9800;"><strong>Altos (≤15 días):</strong> {productos_por_vencer['altos']}</span>
                        <span style="color: #ffc107;"><strong>Medios (≤30 días):</strong> {productos_por_vencer['medios']}</span>
                    </div>
        """
        
        if productos_por_vencer['total_productos'] > 0:
            html_content += """
                    <table style="width: 100%; margin-top: 10px;">
                        <tr style="background: #ffcc02;">
                            <th>Producto</th><th>Lote</th><th>Vencimiento</th><th>Días Restantes</th><th>Cantidad</th><th>Urgencia</th>
                        </tr>
            """
            for item in productos_por_vencer['detalle']:
                urgencia_color = '#f44336' if item['urgencia'] == 'critica' else '#ff9800' if item['urgencia'] == 'alta' else '#ffc107'
                urgencia_texto = 'CRÍTICA' if item['urgencia'] == 'critica' else 'ALTA' if item['urgencia'] == 'alta' else 'MEDIA'
                html_content += f"""
                        <tr>
                            <td>{item['producto'].nombreProducto}</td>
                            <td>{item['lote'].codigo_lote}</td>
                            <td>{item['fecha_vencimiento'].strftime('%d/%m/%Y')}</td>
                            <td style="color: {urgencia_color}; font-weight: bold;">{item['dias_restantes']} días</td>
                            <td style="text-align: center;">{item['cantidad_disponible']}</td>
                            <td style="color: {urgencia_color}; font-weight: bold;">{urgencia_texto}</td>
                        </tr>
                """
            html_content += "</table>"
        else:
            html_content += '<p style="color: #4caf50; text-align: center; margin: 0;">No hay productos próximos a vencer</p>'
        
        html_content += "</div>"
        
        html_content += """
                
                <h2>Reabastecimientos Recientes (Ultima Semana)</h2>
                <table>
                    <tr><th>Fecha</th><th>Producto</th><th>Cantidad</th><th>Lote</th><th>Vencimiento</th></tr>
        """
        
        for reab in reabastecimientos:
            html_content += f"""
                <tr>
                    <td>{reab.fecha.strftime('%d/%m/%Y')}</td>
                    <td>{reab.producto.nombreProducto}</td>
                    <td style="color: #2e7d32; font-weight: bold;">+{reab.cantidad}</td>
                    <td>{reab.lote or '-'}</td>
                    <td>{reab.fecha_vencimiento.strftime('%d/%m/%Y') if reab.fecha_vencimiento else '-'}</td>
                </tr>
            """
        
        html_content += """
                </table>
                
                <h2>Ultimos 15 Pedidos</h2>
                <table>
                    <tr><th>#</th><th>Cliente</th><th>Total</th><th>Estado</th><th>Fecha</th></tr>
        """
        
        for ped in pedidos_recientes:
            estado_color = '#2e7d32' if ped.estado == 'Entregado' else '#f57c00' if ped.estado == 'En camino' else '#1976d2'
            html_content += f"""
                <tr>
                    <td>{ped.idPedido}</td>
                    <td>{ped.idCliente.nombre if ped.idCliente else 'N/A'}</td>
                    <td style="font-weight: bold;">${ped.total:,.0f}</td>
                    <td style="color: {estado_color};">{ped.estado}</td>
                    <td>{ped.fechaCreacion.strftime('%d/%m/%Y %H:%M')}</td>
                </tr>
            """
        
        html_content += f"""
                </table>
                
                <h2>Repartidores y Entregas</h2>
                <div class="highlight" style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left-color: #4caf50;">
                    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center;">
                        <div style="padding: 10px;">
                            <div style="font-size: 2rem; font-weight: bold; color: #2e7d32;">{total_entregas_confirmadas}</div>
                            <div style="color: #666;">Entregas Confirmadas (Mes)</div>
                        </div>
                        <div style="padding: 10px;">
                            <div style="font-size: 2rem; font-weight: bold; color: #2e7d32;">{promedio_calificacion_general:.1f}/5</div>
                            <div style="color: #666;">Calificacion Promedio</div>
                        </div>
                    </div>
        """
        
        if repartidor_estrella:
            html_content += f"""
                    <div style="margin-top: 15px; padding: 15px; background: white; border-radius: 10px; text-align: center;">
                        <div style="font-size: 1.2rem; color: #fbc02d; margin-bottom: 5px;">ESTRELLA DEL MES</div>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #2e7d32;">{repartidor_estrella['repartidor__nombreRepartidor']}</div>
                        <div style="color: #666;">Promedio: {repartidor_estrella['promedio']:.1f}/5 | {repartidor_estrella['entregas']} entregas</div>
                    </div>
            """
        
        html_content += f"""
                </div>
                
                <div class="footer">
                    <p style="font-size: 0.9rem;">Este reporte fue generado automaticamente desde el Dashboard de Glam Store</p>
                    <p style="font-size: 0.8rem; color: #bbb;">{ahora.strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # === ENVIAR CORREO ===
        try:
            # Obtener el email del administrador logueado
            usuario_id = request.session.get('usuario_id')
            email_admin = None
            
            if usuario_id:
                try:
                    usuario = Usuario.objects.get(idUsuario=usuario_id)
                    email_admin = usuario.email
                except Usuario.DoesNotExist:
                    pass
            
            # Si no se pudo obtener el email del admin, usar el de glamstore por defecto
            if not email_admin:
                email_admin = settings.EMAIL_HOST_USER
            
            subject = f'Reporte Dashboard Glam Store - {ahora.strftime("%d/%m/%Y")}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [email_admin]  # Enviar al admin logueado
            
            print(f"DEBUG - Enviando reporte:")
            print(f"  From: {from_email}")
            print(f"  To: {to_email}")
            print(f"  Subject: {subject}")
            
            text_content = f'Reporte del Dashboard generado el {ahora.strftime("%d/%m/%Y %H:%M")}'
            
            email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()
            
            print("DEBUG - Correo enviado exitosamente")
            messages.success(request, f'Reporte enviado exitosamente a {email_admin}')
        except Exception as email_error:
            print(f"ERROR al enviar correo: {str(email_error)}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error al enviar el correo: {str(email_error)}')
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        messages.error(request, f'Error al generar el reporte: {str(e)}')
    
    return redirect('dashboard_admin')

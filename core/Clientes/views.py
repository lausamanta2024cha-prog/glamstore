from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from core.models import Categoria, Subcategoria, Producto, Cliente
import time
from django.db import connection, models
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string 
from django.contrib.auth.hashers import make_password
from core.models import Pedido, Usuario
from .forms import LoginForm
from .services import autenticar_usuario
from core.models import MovimientoProducto
from django.db import transaction
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta

# ✅ Función auxiliar: obtiene el carrito actual desde sesión
def obtener_carrito_actual(request):
    carrito = request.session.get('carrito', {})
    carrito_convertido = {}
    for k, v in carrito.items():
        try:
            carrito_convertido[int(k)] = int(v)
        except (ValueError, TypeError):
            continue
    return carrito_convertido

# ✅ Vista principal de la tienda
def tienda(request):
    categorias = Categoria.objects.all()
    productos_destacados = Producto.objects.all().order_by('-idProducto')[:12] # Muestra los 12 productos más nuevos
    
    return render(request, 'tienda.html', {
        'categorias': categorias,
        'productos_destacados': productos_destacados
    })
# ✅ Vista del perfil del usuario
def perfil(request):
    # Manejar edición de perfil si es POST
    if request.method == 'POST' and request.POST.get('action') == 'editar_perfil':
        return handle_editar_perfil(request)
    
    usuario_id = request.session.get('usuario_id')

    # Priorizar siempre al usuario logueado
    if usuario_id:
        try:
            usuario = get_object_or_404(Usuario, idUsuario=usuario_id)
            # Asegurarse de que el usuario tenga un cliente asociado
            if not usuario.idCliente:
                messages.error(request, "Tu cuenta de usuario no está vinculada a un perfil de cliente.")
                return redirect('tienda')
            
            cliente = get_object_or_404(Cliente, idCliente=usuario.idCliente)
            tiene_usuario = True
            sin_sesion = False

        except (Usuario.DoesNotExist, Cliente.DoesNotExist, Http404):
            messages.error(request, "No se pudo encontrar tu perfil. Por favor, inicia sesión de nuevo.")
            # Limpiar sesión corrupta
            request.session.flush()
            return redirect('login')
    
    # Si no hay usuario, ver si es un cliente invitado
    else:
        cliente_id = request.session.get('cliente_id')
        if cliente_id:
            try:
                cliente = get_object_or_404(Cliente, idCliente=cliente_id)
                
                # IMPORTANTE: Verificar si este cliente ya tiene un usuario en la BD
                usuario_existente = Usuario.objects.filter(idCliente=cliente.idCliente).first()
                if usuario_existente:
                    # El cliente ya tiene usuario, pero no está en sesión
                    # Esto puede pasar si hizo logout y luego hizo un pedido como invitado
                    tiene_usuario = True
                else:
                    # Es un verdadero cliente invitado sin usuario
                    tiene_usuario = False
                
                sin_sesion = False
            except (Cliente.DoesNotExist, Http404):
                messages.error(request, "No se pudo encontrar tu perfil de invitado.")
                # Limpiar ID de cliente inválido
                del request.session['cliente_id']
                return redirect('tienda')
        # Si no hay ni usuario ni invitado, es sin sesión
        else:
            return render(request, 'perfil.html', {'sin_sesion': True})

    # Verificar y actualizar pedidos automáticamente
    from django.utils import timezone
    from datetime import timedelta
    
    # Buscar pedidos que están en camino (incluyendo los de pago parcial con repartidor)
    pedidos_en_camino = Pedido.objects.filter(
        idCliente=cliente.idCliente
    ).filter(
        models.Q(estado='En Camino') | 
        models.Q(estado='Pago Parcial', idRepartidor__isnull=False)
    )
    
    ahora = timezone.now()
    for pedido in pedidos_en_camino:
        # Calcular fecha de entrega
        direccion_lower = (cliente.direccion or "").lower()
        if 'soacha' in direccion_lower:
            dias_entrega = 3
        elif 'bogota' in direccion_lower or 'bogotá' in direccion_lower:
            dias_entrega = 2
        else:
            dias_entrega = 3
        
        fecha_entrega = pedido.fechaCreacion + timedelta(days=dias_entrega)
        
        # Si ya pasó la fecha de entrega, marcar como entregado
        if ahora >= fecha_entrega:
            # Al entregar, el pago se completa automáticamente (se cobró el envío)
            pedido.estado_pedido = 'Entregado'
            pedido.save()
    
    # Obtener los pedidos del cliente determinado
    pedidos = Pedido.objects.filter(idCliente=cliente.idCliente).order_by('-fechaCreacion')
    
    # Verificar si hay pedidos entregados sin confirmar
    pedidos_entregados_sin_confirmar = pedidos.filter(estado_pedido='Entregado')

    context = {
        'cliente': cliente,
        'pedidos': pedidos,
        'tiene_usuario': tiene_usuario,
        'sin_sesion': sin_sesion,
        'pedidos_entregados_sin_confirmar': pedidos_entregados_sin_confirmar
    }
    return render(request, 'perfil.html', context)

# ✅ Vista del carrito: muestra productos, totales y categoría
def carrito(request):
    carrito_raw = obtener_carrito_actual(request)
    carrito = []
    total = 0
    categoria_id = None

    for id_producto, cantidad in carrito_raw.items():
        try:
            producto = Producto.objects.get(idProducto=id_producto)
            subtotal = producto.precio_venta * cantidad
            total += subtotal
            producto.rango_cantidad = range(1, max(producto.stock - cantidad + 1, 1))  # Para el selector
            carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            if not categoria_id:
                categoria_id = producto.idCategoria_id
        except Producto.DoesNotExist:
            continue

    context = {
        'carrito': carrito,
        'total': total,
        'categoria_id': categoria_id
    }
    return render(request, 'carrito.html', context)

# ✅ Vista por categoría: filtra productos y ajusta stock disponible
def productos_por_categoria(request, id_categoria):
    categoria = Categoria.objects.get(idCategoria=id_categoria)
    subcategorias = Subcategoria.objects.filter(categoria_id=id_categoria)
    productos = Producto.objects.filter(idCategoria_id=id_categoria)

    id_sub = request.GET.get('subcategoria')
    subcategoria = None
    if id_sub:
        subcategoria = Subcategoria.objects.filter(idSubcategoria=id_sub).first()
        productos = productos.filter(idSubcategoria_id=id_sub)

    carrito_actual = obtener_carrito_actual(request)

    for producto in productos:
        en_carrito = int(carrito_actual.get(producto.idProducto, 0))
        producto.en_carrito = en_carrito
        producto.disponible = max(producto.stock - en_carrito, 0)
        producto.rango_cantidad = range(1, producto.disponible + 1)

    context = {
        'categoria': categoria,
        'categorias': Categoria.objects.all(),
        'subcategorias': subcategorias,
        'subcategoria': subcategoria,
        'productos': productos,
        'carrito_actual': carrito_actual,
        'range': range(0, 100)
    }
    return render(request, 'productos_categoria.html', context)

# ✅ Vista por subcategoría (puedes expandirla con filtros)
def productos_por_subcategoria(request, nombreSubcategoria):
    subcategoria = Subcategoria.objects.filter(nombreSubcategoria__iexact=nombreSubcategoria).first()
    productos = Producto.objects.filter(idSubcategoria=subcategoria) if subcategoria else []

    return render(request, 'productos_subcategoria.html', {
        'subcategoria': subcategoria,
        'productos': productos
    })

# ✅ Agrega productos al carrito con validación de stock
@csrf_exempt
def agregar_al_carrito(request):
    if request.method == 'POST':
        idProducto = int(request.POST.get('idProducto'))
        cantidad = int(request.POST.get('cantidad', 1))

        try:
            producto = Producto.objects.get(idProducto=idProducto)
        except Producto.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Producto no encontrado.'
                })
            messages.error(request, "Producto no encontrado.")
            return redirect('tienda')

        carrito = request.session.get('carrito', {})
        actual = int(carrito.get(str(idProducto), 0))

        if actual + cantidad > producto.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'No hay suficiente stock disponible.'
                })
            messages.error(request, "No hay suficiente stock disponible.")
            return redirect('productos_categoria', id_categoria=producto.idCategoria_id)

        carrito[str(idProducto)] = actual + cantidad
        request.session['carrito'] = carrito
        
        # Calcular el total de items en el carrito
        cart_count = sum(int(qty) for qty in carrito.values())

        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{producto.nombreProducto} añadido al carrito.',
                'cart_count': cart_count
            })

        # Si no es AJAX, comportamiento normal
        messages.success(request, "Producto añadido al carrito.")
        return redirect('productos_categoria', id_categoria=producto.idCategoria_id)


# ✅ Actualiza la cantidad de un producto en el carrito (AJAX)
@csrf_exempt
def actualizar_cantidad_carrito(request):
    if request.method == 'POST':
        idProducto = str(request.POST.get('idProducto'))
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        
        try:
            producto = Producto.objects.get(idProducto=idProducto)
        except Producto.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Producto no encontrado.'})
            messages.error(request, "Producto no encontrado.")
            return redirect('ver_carrito')
        
        # Validar que la cantidad no exceda el stock
        if nueva_cantidad > producto.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'No hay suficiente stock disponible.'})
            messages.error(request, "No hay suficiente stock disponible.")
            return redirect('ver_carrito')
        
        # Actualizar el carrito
        carrito = request.session.get('carrito', {})
        if nueva_cantidad > 0:
            carrito[idProducto] = nueva_cantidad
        else:
            # Si la cantidad es 0, eliminar del carrito
            if idProducto in carrito:
                del carrito[idProducto]
        
        request.session['carrito'] = carrito
        
        # Calcular nuevo subtotal y total
        subtotal = producto.precio_venta * nueva_cantidad
        total_carrito = sum(
            Producto.objects.get(idProducto=pid).precio_venta * int(qty)
            for pid, qty in carrito.items()
        )
        cart_count = sum(int(qty) for qty in carrito.values())
        
        # Si es AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'subtotal': subtotal,
                'total': total_carrito,
                'cart_count': cart_count
            })
        
        messages.success(request, "Cantidad actualizada.")
        return redirect('ver_carrito')
    
    return redirect('ver_carrito')


# ✅ Elimina un producto del carrito
@csrf_exempt
def eliminar_del_carrito(request):
    if request.method == 'POST':
        idProducto = request.POST.get('idProducto')
        carrito = request.session.get('carrito', {})

        if idProducto in carrito:
            del carrito[idProducto]
            request.session['carrito'] = carrito
            messages.success(request, "Producto eliminado del carrito.")
        else:
            messages.error(request, "El producto no estaba en el carrito.")

    return redirect('ver_carrito')

# ✅ Vacía todo el carrito
@csrf_exempt
def vaciar_carrito(request):
    request.session['carrito'] = {}
    messages.success(request, "Carrito vaciado con éxito.")
    return redirect('ver_carrito')

from datetime import datetime
from django.db import transaction
from core.models import DetallePedido

def simular_pago(request):
    carrito_raw = request.session.get('carrito', {})
    if not carrito_raw:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')

    try:
        with transaction.atomic():
            # 1. Obtener o crear el cliente con los datos del formulario
            correo = request.POST.get('correo')
            nombre = request.POST.get('nombre')
            apellidos = request.POST.get('apellidos')
            documento = request.POST.get('documento')
            telefono = request.POST.get('telefono')
            
            # DEBUG: Imprimir datos recibidos
            print(f"DEBUG - Datos recibidos:")
            print(f"  Correo: {correo}")
            print(f"  Nombre: {nombre} {apellidos}")
            print(f"  Documento: {documento}")
            print(f"  Teléfono: {telefono}")
            
            # Datos de entrega
            departamento = request.POST.get('departamento')
            municipio = request.POST.get('municipio')
            comuna = request.POST.get('comuna')
            direccion = request.POST.get('direccion')
            info_adicional = request.POST.get('info_adicional', '')
            
            # Construir dirección completa
            direccion_completa = f"{direccion}, {comuna}, {municipio}, {departamento}"
            if info_adicional:
                direccion_completa += f" ({info_adicional})"
            
            print(f"  Dirección completa: {direccion_completa}")
            print(f"  Longitud dirección: {len(direccion_completa)} caracteres")
            
            # Buscar si ya existe un cliente con ese email
            try:
                cliente = Cliente.objects.get(email=correo)
                print(f"DEBUG - Cliente existente encontrado: ID {cliente.idCliente}")
                # Actualizar datos del cliente
                cliente.nombre = f"{nombre} {apellidos}"
                cliente.cedula = documento
                cliente.telefono = telefono
                cliente.direccion = direccion_completa
                cliente.save()
                print(f"DEBUG - Cliente actualizado exitosamente")
            except Cliente.DoesNotExist:
                print(f"DEBUG - Creando nuevo cliente...")
                # Crear nuevo cliente
                cliente = Cliente.objects.create(
                    email=correo,
                    nombre=f"{nombre} {apellidos}",
                    cedula=documento,
                    telefono=telefono,
                    direccion=direccion_completa
                )
                print(f"DEBUG - Cliente creado exitosamente: ID {cliente.idCliente}")

            # 2. Calcular el total y preparar los detalles del pedido
            total_pedido = 0
            detalles_para_crear = []
            for id_str, cantidad in carrito_raw.items():
                producto = Producto.objects.get(idProducto=int(id_str))
                if producto.stock < cantidad:
                    raise Exception(f"No hay suficiente stock para {producto.nombreProducto}")
                
                subtotal = producto.precio_venta * cantidad
                total_pedido += subtotal
                detalles_para_crear.append((producto, cantidad, subtotal))

            # Decidir el estado y el total final basado en el pago del envío
            from decimal import Decimal
            pago_envio = request.POST.get('pago_envio', 'ahora')
            costo_envio = 10000
            tasa_iva = Decimal('0.19')  # 19% de IVA
            
            # Calcular IVA sobre el subtotal de productos (sin incluir envío)
            iva = int(total_pedido * tasa_iva)
            
            # El total y estado dependen del tipo de pago
            if pago_envio == 'ahora':
                # Cliente pagó todo (productos + IVA + envío)
                total_final = int(total_pedido) + iva + costo_envio
                estado_pago = 'Pago Completo'
            else:
                # Cliente pagó solo productos + IVA, envío contra entrega
                total_final = int(total_pedido) + iva
                estado_pago = 'Pago Parcial'

            print(f"DEBUG - Creando pedido:")
            print(f"  Subtotal productos: {total_pedido}")
            print(f"  IVA (19%): {iva}")
            print(f"  Envío: {costo_envio if pago_envio == 'ahora' else 0}")
            print(f"  Total final: {total_final}")
            print(f"  Estado Pago: {estado_pago}")

            # 3. Crear el Pedido principal en la base de datos
            nuevo_pedido = Pedido.objects.create(
                idCliente=cliente,
                estado_pago=estado_pago,
                estado_pedido='Confirmado',
                total=total_final,
                fechaCreacion=datetime.now()
            )
            
            print(f"DEBUG - Pedido creado exitosamente: ID {nuevo_pedido.idPedido}")

            # 4. Crear los Detalles del Pedido y actualizar el stock de productos
            for producto, cantidad, subtotal in detalles_para_crear:
                DetallePedido.objects.create(
                    idPedido=nuevo_pedido,
                    idProducto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio_venta,
                    subtotal=subtotal
                )
                producto.stock -= cantidad
                MovimientoProducto.objects.create(
                    producto=producto,
                    tipo_movimiento='SALIDA_VENTA',
                    precio_unitario=producto.precio_venta,
                    cantidad=cantidad,
                    stock_anterior=producto.stock + cantidad,
                    stock_nuevo=producto.stock,
                    id_pedido=nuevo_pedido,
                    descripcion=f'Venta en pedido #{nuevo_pedido.idPedido}'
                )
                producto.save()

        # 5. NO guardar sesión automáticamente - solo si ya tiene usuario_id
        # Si el usuario ya estaba logueado, mantener su sesión
        # Si no estaba logueado, NO crear sesión automática
        
        print(f"DEBUG - Pedido creado sin iniciar sesión automática")
        
        # 6. Limpiar el carrito y redirigir a confirmación
        request.session['carrito'] = {}
        
        # Guardar el ID del pedido temporalmente para mostrar la confirmación
        request.session['ultimo_pedido_id'] = nuevo_pedido.idPedido
        
        messages.success(request, f"¡Pedido exitoso! Tu pedido #{nuevo_pedido.idPedido} ha sido registrado.")
        return redirect('pedido_confirmado', idPedido=nuevo_pedido.idPedido)

    except Exception as e:
        print(f"ERROR - Excepción capturada: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        messages.error(request, f"Ocurrió un error al procesar tu pedido: {e}")
        return redirect('ver_carrito')

# ✅ Finaliza la compra sin simulación (opcional)
def finalizar_compra(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')

    request.session['carrito'] = {}
    messages.success(request, "¡Compra finalizada con éxito! Gracias por tu confianza pastel-glam.")
    return redirect('tienda')

# ✅ Vista de depuración para ver el carrito en consola
def ver_carrito_debug(request):
    carrito_raw = obtener_carrito_actual(request)
    carrito = []
    total = 0

    for id_producto, cantidad in carrito_raw.items():
        try:
            producto = Producto.objects.get(idProducto=id_producto)
            subtotal = producto.precio_venta * cantidad
            total += subtotal
            carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            continue

    print("CARRITO ACTUAL:", carrito_raw)
    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total
    })
import random
import string

def generar_codigo_pago():
    return 'GLAM-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def checkout(request):
    carrito_raw = request.session.get('carrito', {})
    if not carrito_raw:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')

    carrito = []
    total = 0

    for id_producto, cantidad in carrito_raw.items():
        try:
            producto = Producto.objects.get(idProducto=id_producto)
            subtotal = producto.precio_venta * cantidad
            total += subtotal
            carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            continue

    # Verificar si el usuario está logueado y obtener sus datos
    usuario_logueado = None
    cliente_datos = None
    
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario_logueado = Usuario.objects.get(idUsuario=usuario_id)
            if usuario_logueado.idCliente:
                cliente_datos = Cliente.objects.get(idCliente=usuario_logueado.idCliente)
        except (Usuario.DoesNotExist, Cliente.DoesNotExist):
            pass

    context = {
        'carrito': carrito,
        'total': total,
        'usuario_logueado': usuario_logueado,
        'cliente_datos': cliente_datos
    }
    return render(request, 'checkout.html', context)

def registro(request):
    if request.method == 'POST':
        # 1. Obtener datos del formulario
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar_password = request.POST.get('confirmar_password')
        cedula = request.POST.get('cedula')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')

        # 2. Validaciones
        if password != confirmar_password:
            messages.error(request, "Las contraseñas no coinciden.", extra_tags='login')
            return render(request, 'registrar_usuario.html', {'input': request.POST})

        # Validar longitud mínima de contraseña
        if len(password) < 6:
            messages.error(request, "La contraseña debe tener al menos 6 caracteres.", extra_tags='login')
            return render(request, 'registrar_usuario.html', {'input': request.POST})

        # Verificar si ya existe un usuario con este email
        # Nota: Si solo existe un Cliente (sin Usuario), se permite el registro
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya tiene una cuenta registrada. Por favor, inicia sesión.", extra_tags='login')
            return render(request, 'registrar_usuario.html', {'input': request.POST})

        try:
            with transaction.atomic():
                # 3. Verificar si ya existe un cliente con este email (pedido como invitado)
                cliente_existente = Cliente.objects.filter(email=email).first()
                
                if cliente_existente:
                    # El cliente ya existe (hizo pedido como invitado)
                    # Actualizar sus datos con la información del registro
                    cliente_existente.nombre = nombre
                    cliente_existente.cedula = cedula
                    cliente_existente.direccion = direccion
                    cliente_existente.telefono = telefono
                    cliente_existente.save()
                    
                    cliente = cliente_existente
                    messages.info(request, "Encontramos tus pedidos anteriores. ¡Ahora puedes hacer seguimiento!")
                else:
                    # Crear nuevo cliente
                    cliente = Cliente.objects.create(
                        nombre=nombre,
                        email=email,
                        cedula=cedula,
                        direccion=direccion,
                        telefono=telefono
                    )

                # 4. Crear el Usuario asociado con rol de Cliente (rol=2)
                Usuario.objects.create(
                    nombre=nombre,
                    email=email,
                    password=make_password(password),
                    id_rol=2,  # Rol de Cliente
                    idCliente=cliente.idCliente
                )

            messages.success(request, "¡Registro exitoso! Ahora puedes iniciar sesión.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Ocurrió un error durante el registro: {e}", extra_tags='login')

    return render(request, 'registrar_usuario.html')




def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['usuario']
        password = form.cleaned_data['password']

        # Diagnóstico: imprimir lo que se recibe
        print("Email recibido:", email)
        print("Password recibido:", password)

        usuario = autenticar_usuario(email, password)

        if usuario:
            print("Usuario autenticado:", usuario)  # Confirmación de autenticación

            # Limpiar cualquier sesión de cliente invitado previa
            if 'cliente_id' in request.session:
                del request.session['cliente_id']
            if 'cliente_nombre' in request.session:
                del request.session['cliente_nombre']

            request.session['usuario_id'] = usuario['id']
            request.session['usuario_nombre'] = usuario['nombre']
            request.session['usuario_rol'] = usuario['rol']

            if usuario['rol'] == 1:
                return redirect('dashboard_admin')
            elif usuario['rol'] == 2:
                return redirect('tienda')
        else:
            print("Autenticación fallida")  # Si no pasa la verificación
            messages.error(request, "Correo o contraseña incorrectos.", extra_tags='login')

    return render(request, 'login.html', {'form': form})



def recuperar_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
            token = get_random_string(length=32)
            
            # Guardar el token y la fecha de expiración en la base de datos
            usuario.reset_token = token
            usuario.reset_token_expires = timezone.now() + timedelta(hours=1)
            usuario.save(update_fields=['reset_token', 'reset_token_expires'])

            link = request.build_absolute_uri(reverse('cambiar_password', args=[token]))
            
            # Crear el correo HTML profesional
            html_message = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; margin: 0; padding: 0; }}
                    .container {{ max-width: 600px; margin: 20px auto; background-color: #ffffff; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-radius: 12px; overflow: hidden; }}
                    .header {{ background: linear-gradient(135deg, #d946a6 0%, #c026d3 100%); color: white; padding: 50px 20px; text-align: center; }}
                    .header h1 {{ margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.5px; }}
                    .header p {{ margin: 10px 0 0 0; font-size: 15px; opacity: 0.95; font-weight: 300; }}
                    .content {{ padding: 45px 35px; }}
                    .content h2 {{ color: #d946a6; font-size: 22px; margin-top: 0; margin-bottom: 18px; font-weight: 600; }}
                    .content p {{ color: #555; font-size: 15px; line-height: 1.7; margin: 16px 0; }}
                    .alert {{ background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%); border-left: 5px solid #d946a6; padding: 18px; margin: 25px 0; border-radius: 6px; }}
                    .alert p {{ color: #880e4f; margin: 0; font-size: 14px; font-weight: 500; }}
                    .button-container {{ text-align: center; margin: 35px 0; }}
                    .button {{ display: inline-block; background: linear-gradient(135deg, #d946a6 0%, #c026d3 100%); color: white; padding: 16px 48px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(217, 70, 166, 0.3); }}
                    .button:hover {{ transform: translateY(-3px); box-shadow: 0 6px 16px rgba(217, 70, 166, 0.4); }}
                    .link-text {{ color: #666; font-size: 12px; word-break: break-all; margin-top: 15px; padding: 12px; background-color: #f5f5f5; border-radius: 6px; border: 1px solid #e0e0e0; }}
                    .footer {{ background: linear-gradient(135deg, #f8f9fa 0%, #f0f0f0 100%); padding: 25px; text-align: center; border-top: 1px solid #e0e0e0; }}
                    .footer p {{ color: #888; font-size: 12px; margin: 6px 0; }}
                    .security-info {{ background: linear-gradient(135deg, #f3e5f5 0%, #ede7f6 100%); border-left: 5px solid #c026d3; padding: 18px; margin: 25px 0; border-radius: 6px; }}
                    .security-info p {{ color: #6a1b9a; margin: 0; font-size: 14px; font-weight: 500; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Recuperación de Contraseña</h1>
                        <p>Glam Store — Tu tienda de belleza</p>
                    </div>
                    
                    <div class="content">
                        <h2>Hola,</h2>
                        <p>Recibimos una solicitud para recuperar tu contraseña en Glam Store. Si no fuiste tú, puedes ignorar este correo de forma segura.</p>
                        
                        <p>Para cambiar tu contraseña, haz clic en el botón de abajo:</p>
                        
                        <div class="button-container">
                            <a href="{link}" class="button">Cambiar Contraseña</a>
                        </div>
                        
                        <p style="text-align: center; color: #999; font-size: 13px;">O copia y pega este enlace en tu navegador:</p>
                        <div class="link-text">{link}</div>
                        
                        <div class="alert">
                            <p><strong>Este enlace expira en 1 hora</strong> por razones de seguridad. Si no cambias tu contraseña en ese tiempo, deberás solicitar un nuevo enlace.</p>
                        </div>
                        
                        <div class="security-info">
                            <p><strong>Información de seguridad:</strong> Nunca compartiremos tu contraseña por correo. Si no solicitaste este cambio, cambia tu contraseña inmediatamente desde tu cuenta.</p>
                        </div>
                        
                        <p style="margin-top: 30px; color: #666; font-size: 14px;">
                            Si tienes problemas para acceder a tu cuenta o necesitas ayuda, contáctanos en <strong>soporte@glamstore.com</strong>
                        </p>
                    </div>
                    
                    <div class="footer">
                        <p><strong>Glam Store</strong> — Tu espacio de moda, color y elegancia</p>
                        <p>© 2025 Glam Store. Todos los derechos reservados.</p>
                        <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            send_mail(
                subject="Recuperación de Contraseña — Glam Store",
                message=f"Haz clic en el siguiente enlace para cambiar tu contraseña:\n{link}",
                from_email="no-reply@glamstore.com",
                recipient_list=[email],
                html_message=html_message,
            )
            
            messages.success(request, "Te hemos enviado un enlace de recuperación a tu correo.")
        except Usuario.DoesNotExist:
            messages.error(request, "Este correo no está registrado.")
            
    return render(request, 'recuperar_password.html')

def cambiar_password(request, token):
    try:
        usuario = Usuario.objects.get(reset_token=token, reset_token_expires__gt=timezone.now())
    except Usuario.DoesNotExist:
        messages.error(request, "Token inválido o expirado.")
        return redirect('login')

    if request.method == 'POST':
        nueva = request.POST.get('nueva')
        confirmacion = request.POST.get('confirmacion')

        if nueva and nueva == confirmacion:
            if len(nueva) < 6:
                messages.error(request, "La contraseña debe tener al menos 6 caracteres.", extra_tags='login')
                return render(request, 'cambiar_password.html')

            usuario.password = make_password(nueva)
            usuario.reset_token = None
            usuario.reset_token_expires = None
            usuario.save(update_fields=['password', 'reset_token', 'reset_token_expires'])
            
            messages.success(request, "Tu contraseña ha sido actualizada.", extra_tags='login')
            return redirect('login')
        else:
            messages.error(request, "Las contraseñas no coinciden o están vacías.", extra_tags='login')

    return render(request, 'cambiar_password.html')



def autenticar_usuario(email, password):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT idUsuario, password, nombre, id_rol FROM usuarios
            WHERE email = %s
        """, [email])
        usuario = cursor.fetchone()

    if usuario and check_password(password, usuario[1]):
        return {
            'id': usuario[0],
            'nombre': usuario[2],
            'rol': usuario[3]
        }
    return None





def registrar_usuario(request):
    return HttpResponse("Página de registro en construcción")


from django.shortcuts import render
from django.http import HttpResponse

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        # Enviar correo
        subject = f"Nuevo mensaje de contacto de {nombre}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.EMAIL_HOST_USER]

        html_content = render_to_string('email_contacto.html', {
            'nombre': nombre,
            'email': email,
            'mensaje': mensaje
        })
        text_content = strip_tags(html_content)

        email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        messages.success(request, "Tu mensaje ha sido enviado. ¡Gracias por contactarnos!")
        return redirect('contacto')

    return render(request, 'contacto.html')

def crear_usuario_desde_cliente(request):
    """
    Vista para que un cliente invitado cree su usuario/contraseña
    """
    if request.method == 'POST':
        cliente_id = request.session.get('cliente_id')
        
        if not cliente_id:
            messages.error(request, "No se encontró información de cliente.")
            return redirect('login')
        
        try:
            cliente = Cliente.objects.get(idCliente=cliente_id)
            
            # Verificar si ya tiene un usuario
            if Usuario.objects.filter(idCliente=cliente_id).exists():
                messages.warning(request, "Ya tienes un usuario creado. Puedes iniciar sesión.")
                return redirect('login')
            
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            # Validar que las contraseñas coincidan
            if password != password_confirm:
                messages.error(request, "Las contraseñas no coinciden.")
                return redirect('perfil')
            
            # Validar longitud mínima
            if len(password) < 6:
                messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
                return redirect('perfil')
            
            # Crear el usuario
            nuevo_usuario = Usuario.objects.create(
                nombre=cliente.nombre,
                email=cliente.email,
                password=make_password(password),
                id_rol=2,  # Rol de Cliente
                idCliente=cliente.idCliente
            )
            
            # Loguear automáticamente al usuario
            request.session['usuario_id'] = nuevo_usuario.idUsuario
            request.session['usuario_nombre'] = nuevo_usuario.nombre
            request.session['usuario_rol'] = 2
            
            # Limpiar el cliente_id de invitado
            if 'cliente_id' in request.session:
                del request.session['cliente_id']
            if 'cliente_nombre' in request.session:
                del request.session['cliente_nombre']
            
            messages.success(request, "¡Cuenta creada exitosamente! Ahora puedes iniciar sesión cuando quieras.")
            return redirect('perfil')
            
        except Cliente.DoesNotExist:
            messages.error(request, "Cliente no encontrado.")
            return redirect('tienda')
        except Exception as e:
            messages.error(request, f"Error al crear la cuenta: {e}")
            return redirect('perfil')
    
    return redirect('perfil')

def pedido_confirmado(request, idPedido):
    """
    Vista para ver la confirmación de un pedido (solo detalles).
    - Usuarios registrados: pueden ver cualquier pedido suyo
    - Sin sesión: solo pueden ver el pedido que acaban de hacer (ultimo_pedido_id)
    """
    pedido = get_object_or_404(Pedido, idPedido=idPedido)
    
    # Verificar permisos de acceso
    usuario_id = request.session.get('usuario_id')
    ultimo_pedido_id = request.session.get('ultimo_pedido_id')
    
    # Si tiene usuario_id, verificar que el pedido sea suyo
    if usuario_id:
        try:
            usuario = Usuario.objects.get(idUsuario=usuario_id)
            if pedido.idCliente.idCliente != usuario.idCliente:
                messages.error(request, "No tienes permiso para ver este pedido.")
                return redirect('tienda')
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect('login')
    
    # Si no tiene usuario_id, solo puede ver el último pedido que hizo
    elif ultimo_pedido_id == idPedido:
        # Permitir ver el pedido recién creado
        pass
    else:
        # No tiene permiso para ver este pedido
        messages.warning(request, "Para ver el seguimiento de tus pedidos, necesitas iniciar sesión.")
        return redirect('login')
    
    return render(request, 'pedido_confirmado.html', {'pedido': pedido})

def ver_seguimiento(request, idPedido):
    """
    Vista para ver el seguimiento detallado de un pedido (timeline).
    Solo para usuarios registrados.
    """
    # Verificar que el usuario esté logueado
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.warning(request, "Debes iniciar sesión para ver el seguimiento de tus pedidos.")
        return redirect('login')
    
    # Obtener el pedido
    pedido = get_object_or_404(Pedido, idPedido=idPedido)
    
    # Verificar que el pedido pertenezca al usuario
    try:
        usuario = Usuario.objects.get(idUsuario=usuario_id)
        if pedido.idCliente.idCliente != usuario.idCliente:
            messages.error(request, "No tienes permiso para ver este pedido.")
            return redirect('perfil')
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login')
    
    # Calcular fecha de entrega estimada
    from django.utils import timezone
    from datetime import timedelta
    
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
    
    fecha_entrega_estimada = pedido.fechaCreacion + timedelta(days=dias_entrega)
    
    # Obtener los detalles del pedido (productos)
    detalles_pedido = DetallePedido.objects.filter(idPedido=pedido).select_related('idProducto')
    
    # Calcular costo del envío
    costo_envio = 10000
    tasa_iva = 0.19
    
    # Calcular la base líquida (suma de productos sin IVA ni envío)
    # Sumamos los subtotales de los detalles del pedido
    total_productos = sum(detalle.subtotal for detalle in detalles_pedido)
    
    # Determinar si el envío fue pagado
    if pedido.estado_pago == 'Pago Parcial':
        envio_pagado = False
    else:
        envio_pagado = True
    
    context = {
        'pedido': pedido,
        'fecha_entrega_estimada': fecha_entrega_estimada,
        'dias_entrega': dias_entrega,
        'ciudad_entrega': ciudad_entrega,
        'detalles_pedido': detalles_pedido,
        'costo_envio': costo_envio,
        'total_productos': total_productos,
        'envio_pagado': envio_pagado
    }
    
    return render(request, 'ver_seguimiento.html', context)


def handle_editar_perfil(request):
    """
    Función auxiliar para manejar la edición del perfil desde la vista principal
    """
    # Verificar que el usuario esté logueado
    usuario_id = request.session.get('usuario_id')
    cliente_id = request.session.get('cliente_id')
    
    if not usuario_id and not cliente_id:
        messages.error(request, "Debes iniciar sesión para editar tu perfil.")
        return redirect('login')
    
    # Obtener el cliente
    cliente = None
    if usuario_id:
        try:
            usuario = Usuario.objects.get(idUsuario=usuario_id)
            if usuario.idCliente:
                cliente = Cliente.objects.get(idCliente=usuario.idCliente)
        except (Usuario.DoesNotExist, Cliente.DoesNotExist):
            messages.error(request, "No se pudo encontrar tu perfil.")
            return redirect('perfil')
    elif cliente_id:
        try:
            cliente = Cliente.objects.get(idCliente=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, "No se pudo encontrar tu perfil.")
            return redirect('perfil')
    
    if not cliente:
        messages.error(request, "No se pudo encontrar tu perfil.")
        return redirect('perfil')
    
    # Obtener los datos del formulario
    nombre = request.POST.get('nombre', '').strip()
    email = request.POST.get('email', '').strip()
    cedula = request.POST.get('cedula', '').strip()
    telefono = request.POST.get('telefono', '').strip()
    direccion = request.POST.get('direccion', '').strip()
    
    # Validaciones básicas
    if not nombre or not email:
        messages.error(request, "El nombre y el correo son obligatorios.")
        return redirect('perfil')
    
    # Verificar si el email ya existe en otro cliente
    if email != cliente.email:
        if Cliente.objects.filter(email=email).exclude(idCliente=cliente.idCliente).exists():
            messages.error(request, "Este correo electrónico ya está registrado por otro usuario.")
            return redirect('perfil')
    
    try:
        # Actualizar los datos del cliente
        cliente.nombre = nombre
        cliente.email = email
        cliente.cedula = cedula if cedula else None
        cliente.telefono = telefono if telefono else None
        cliente.direccion = direccion if direccion else None
        cliente.save()
        
        # Si hay un usuario asociado, actualizar también su email
        if usuario_id:
            try:
                usuario = Usuario.objects.get(idUsuario=usuario_id)
                usuario.email = email
                usuario.save()
            except Usuario.DoesNotExist:
                pass
        
        messages.success(request, "Tus datos han sido actualizados correctamente.")
        
    except Exception as e:
        messages.error(request, f"Error al actualizar los datos: {str(e)}")
    
    return redirect('perfil')


def editar_perfil(request):
    """
    Vista para editar los datos del perfil del cliente
    """
    if request.method == 'POST':
        # Verificar que el usuario esté logueado
        usuario_id = request.session.get('usuario_id')
        cliente_id = request.session.get('cliente_id')
        
        if not usuario_id and not cliente_id:
            messages.error(request, "Debes iniciar sesión para editar tu perfil.")
            return redirect('login')
        
        # Obtener el cliente
        cliente = None
        if usuario_id:
            try:
                usuario = Usuario.objects.get(idUsuario=usuario_id)
                if usuario.idCliente:
                    cliente = Cliente.objects.get(idCliente=usuario.idCliente)
            except (Usuario.DoesNotExist, Cliente.DoesNotExist):
                messages.error(request, "No se pudo encontrar tu perfil.")
                return redirect('perfil')
        elif cliente_id:
            try:
                cliente = Cliente.objects.get(idCliente=cliente_id)
            except Cliente.DoesNotExist:
                messages.error(request, "No se pudo encontrar tu perfil.")
                return redirect('perfil')
        
        if not cliente:
            messages.error(request, "No se pudo encontrar tu perfil.")
            return redirect('perfil')
        
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        cedula = request.POST.get('cedula', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        
        # Validaciones básicas
        if not nombre or not email:
            messages.error(request, "El nombre y el correo son obligatorios.")
            return redirect('perfil')
        
        # Verificar si el email ya existe en otro cliente
        if email != cliente.email:
            if Cliente.objects.filter(email=email).exclude(idCliente=cliente.idCliente).exists():
                messages.error(request, "Este correo electrónico ya está registrado por otro usuario.")
                return redirect('perfil')
        
        try:
            # Actualizar los datos del cliente
            cliente.nombre = nombre
            cliente.email = email
            cliente.cedula = cedula if cedula else None
            cliente.telefono = telefono if telefono else None
            cliente.direccion = direccion if direccion else None
            cliente.save()
            
            # Si hay un usuario asociado, actualizar también su email
            if usuario_id:
                try:
                    usuario = Usuario.objects.get(idUsuario=usuario_id)
                    usuario.email = email
                    usuario.save()
                except Usuario.DoesNotExist:
                    pass
            
            messages.success(request, "✅ Tus datos han sido actualizados correctamente.")
            
        except Exception as e:
            messages.error(request, f"Error al actualizar los datos: {str(e)}")
        
        return redirect('perfil')
    
    # Si no es POST, redirigir al perfil
    return redirect('perfil')


def confirmar_recepcion_pedido(request, idPedido):
    """
    Vista para que el cliente confirme que recibió su pedido
    """
    pedido = get_object_or_404(Pedido, idPedido=idPedido)
    
    # Verificar que el pedido pertenece al cliente en sesión
    usuario_id = request.session.get('usuario_id')
    cliente_id = request.session.get('cliente_id')
    
    if usuario_id:
        usuario = get_object_or_404(Usuario, idUsuario=usuario_id)
        if pedido.idCliente.idCliente != usuario.idCliente:
            messages.error(request, "No tienes permiso para confirmar este pedido.")
            return redirect('perfil')
    elif cliente_id:
        if pedido.idCliente.idCliente != cliente_id:
            messages.error(request, "No tienes permiso para confirmar este pedido.")
            return redirect('perfil')
    else:
        messages.error(request, "Debes iniciar sesión para confirmar la recepción.")
        return redirect('login')
    
    if request.method == 'POST':
        confirmacion = request.POST.get('confirmacion')
        
        if confirmacion == 'si':
            # Cliente confirma que recibió el pedido
            pedido.estado_pedido = 'Completado'
            pedido.save()
            messages.success(request, f"Gracias por confirmar. El pedido #{pedido.idPedido} ha sido finalizado exitosamente.")
        elif confirmacion == 'no':
            # Cliente indica que no recibió el pedido - mostrar formulario
            return render(request, 'reportar_problema.html', {'pedido': pedido})
        
        return redirect('perfil')
    
    return render(request, 'confirmar_recepcion.html', {'pedido': pedido})


def reportar_problema_entrega(request, idPedido):
    """
    Vista para que el cliente reporte el problema de entrega con detalles
    """
    from core.models import NotificacionProblema
    
    pedido = get_object_or_404(Pedido, idPedido=idPedido)
    
    # Verificar que el pedido pertenece al cliente en sesión
    usuario_id = request.session.get('usuario_id')
    cliente_id = request.session.get('cliente_id')
    
    if usuario_id:
        usuario = get_object_or_404(Usuario, idUsuario=usuario_id)
        if pedido.idCliente.idCliente != usuario.idCliente:
            messages.error(request, "No tienes permiso para reportar este pedido.")
            return redirect('perfil')
    elif cliente_id:
        if pedido.idCliente.idCliente != cliente_id:
            messages.error(request, "No tienes permiso para reportar este pedido.")
            return redirect('perfil')
    else:
        messages.error(request, "Debes iniciar sesión.")
        return redirect('login')
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        foto = request.FILES.get('foto')
        
        if not motivo:
            messages.error(request, "Por favor describe el problema.")
            return render(request, 'reportar_problema.html', {'pedido': pedido})
        
        # Cambiar estado del pedido
        pedido.estado_pedido = 'Problema en Entrega'
        pedido.save()
        
        # Crear notificación
        NotificacionProblema.objects.create(
            idPedido=pedido,
            motivo=motivo,
            foto=foto
        )
        
        messages.warning(request, f"Hemos registrado el problema con el pedido #{pedido.idPedido}. Nuestro equipo se pondrá en contacto contigo.")
        return redirect('perfil')
    
    return render(request, 'reportar_problema.html', {'pedido': pedido})
    return render(request, 'reportar_problema.html', {'pedido': pedido})


def notificaciones_cliente(request):
    """
    Vista para que el cliente vea sus notificaciones de pedidos
    """
    from core.models import NotificacionProblema
    
    usuario_id = request.session.get('usuario_id')
    cliente_id = request.session.get('cliente_id')
    
    if usuario_id:
        usuario = get_object_or_404(Usuario, idUsuario=usuario_id)
        cliente = usuario.idCliente
    elif cliente_id:
        cliente = get_object_or_404(Cliente, idCliente=cliente_id)
    else:
        messages.error(request, "Debes iniciar sesión para ver tus notificaciones.")
        return redirect('login')
    
    # Obtener notificaciones del cliente
    notificaciones = NotificacionProblema.objects.filter(
        idPedido__idCliente=cliente
    ).select_related('idPedido').order_by('-fechaReporte')
    
    return render(request, 'notificaciones_cliente.html', {
        'notificaciones': notificaciones
    })

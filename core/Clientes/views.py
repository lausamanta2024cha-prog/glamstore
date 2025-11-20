from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from core.models import Categoria, Subcategoria, Producto, Cliente
import time
from django.db import connection
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

    # Obtener los pedidos del cliente determinado
    pedidos = Pedido.objects.filter(idCliente=cliente.idCliente).order_by('-fechaCreacion')

    context = {
        'cliente': cliente,
        'pedidos': pedidos,
        'tiene_usuario': tiene_usuario,
        'sin_sesion': sin_sesion
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
            subtotal = producto.precio * cantidad
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
        subtotal = producto.precio * nueva_cantidad
        total_carrito = sum(
            Producto.objects.get(idProducto=pid).precio * int(qty)
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
                
                subtotal = producto.precio * cantidad
                total_pedido += subtotal
                detalles_para_crear.append((producto, cantidad, subtotal))

            # Decidir el estado y el total final basado en el pago del envío
            pago_envio = request.POST.get('pago_envio', 'ahora')
            costo_envio = 10000
            
            if pago_envio == 'ahora':
                estado_pedido = 'Pago Completo'
                total_final = total_pedido + costo_envio
            else:
                estado_pedido = 'Pago Parcial'
                total_final = total_pedido

            print(f"DEBUG - Creando pedido: Total {total_final}, Estado: {estado_pedido}")

            # 3. Crear el Pedido principal en la base de datos
            nuevo_pedido = Pedido.objects.create(
                idCliente=cliente,
                estado=estado_pedido,
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
                    precio_unitario=producto.precio,
                    subtotal=subtotal
                )
                producto.stock -= cantidad
                MovimientoProducto.objects.create(
                    producto=producto,
                    tipo_movimiento='SALIDA_VENTA',
                    precio_unitario=producto.precio,
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
            subtotal = producto.precio * cantidad
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
            subtotal = producto.precio * cantidad
            total += subtotal
            carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            continue

    context = {
        'carrito': carrito,
        'total': total
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
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'registrar_usuario.html', {'input': request.POST})

        # Verificar si ya existe un usuario con este email
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya tiene una cuenta registrada. Por favor, inicia sesión.")
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
            messages.error(request, f"Ocurrió un error durante el registro: {e}")

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

            messages.success(request, f"¡Bienvenida, {usuario['nombre']}!")

            if usuario['rol'] == 1:
                return redirect('dashboard_admin')
            elif usuario['rol'] == 2:
                return redirect('tienda')
        else:
            print("Autenticación fallida")  # Si no pasa la verificación
            messages.error(request, "Correo o contraseña incorrectos.")

    return render(request, 'login.html', {'form': form})



def recuperar_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        with connection.cursor() as cursor:
            cursor.execute("SELECT idUsuario FROM usuarios WHERE email = %s", [email])
            usuario = cursor.fetchone()

        if usuario:
            token = get_random_string(length=32)
            # Guarda el token en una tabla temporal o en la sesión
            request.session['token_recuperacion'] = token
            request.session['usuario_recuperacion'] = usuario[0]

            link = request.build_absolute_uri(f"/cambiar-password/{token}/")
            send_mail(
                subject="Recuperación de contraseña — Glam Store",
                message=f"Haz clic en el siguiente enlace para cambiar tu contraseña:\n{link}",
                from_email="no-reply@glamstore.com",
                recipient_list=[email],
            )
            messages.success(request, "Te hemos enviado un enlace de recuperación a tu correo.")
            return redirect('login')
        else:
            messages.error(request, "Este correo no está registrado.")
    return render(request, 'recuperar_password.html')


def cambiar_password(request, token):
    if request.method == 'POST':
        nueva = request.POST.get('nueva')
        confirmacion = request.POST.get('confirmacion')

        if nueva == confirmacion:
            if token == request.session.get('token_recuperacion'):
                idUsuario = request.session.get('usuario_recuperacion')
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE usuarios SET password = %s WHERE idUsuario = %s
                    """, [make_password(nueva), idUsuario])
                messages.success(request, "Tu contraseña ha sido actualizada.")
                return redirect('login')
            else:
                messages.error(request, "Token inválido o expirado.")
        else:
            messages.error(request, "Las contraseñas no coinciden.")
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
    
    return render(request, 'ver_seguimiento.html', {'pedido': pedido})

  

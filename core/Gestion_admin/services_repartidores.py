from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from datetime import timedelta, time
from core.models.pedidos import Pedido, DetallePedido
from core.models.repartidores import Repartidor
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
import logging
import os
import base64

logger = logging.getLogger(__name__)

HORARIO_INICIO = 6  # 6 AM
HORARIO_FIN = 15    # 3 PM
TIEMPO_ENTREGA_MINUTOS = 120  # 2 horas por pedido
PEDIDOS_POR_REPARTIDOR = (HORARIO_FIN - HORARIO_INICIO) * 60 // TIEMPO_ENTREGA_MINUTOS  # 4 pedidos máximo


def es_dia_habil(fecha):
    """Verifica si es día hábil (lunes a viernes)"""
    return fecha.weekday() < 5  # 0-4 son lunes a viernes


def calcular_fecha_vencimiento(fecha_pedido, ciudad):
    """
    Calcula fecha de vencimiento según ciudad
    - Bogotá: 2 días hábiles
    - Soacha: 3 días hábiles
    """
    dias_vencimiento = 2 if 'bogota' in ciudad.lower() else 3
    
    fecha_actual = fecha_pedido
    dias_contados = 0
    
    while dias_contados < dias_vencimiento:
        fecha_actual += timedelta(days=1)
        if es_dia_habil(fecha_actual):
            dias_contados += 1
    
    return fecha_actual


def obtener_pedidos_sin_asignar(fecha=None):
    """Obtiene los pedidos sin repartidor asignado para una fecha específica"""
    if fecha is None:
        fecha = timezone.now().date()
    
    return Pedido.objects.filter(
        idRepartidor__isnull=True,
        estado_pedido__in=['Confirmado', 'En Preparación'],
        fechaCreacion__date=fecha
    ).select_related('idCliente').order_by('fechaCreacion')


def obtener_repartidores_disponibles():
    """Obtiene los repartidores disponibles"""
    return Repartidor.objects.filter(estado_turno='Disponible').order_by('idRepartidor')


def calcular_capacidad_repartidor(repartidor, fecha=None):
    """Calcula cuántos pedidos más puede tomar un repartidor en un día"""
    if fecha is None:
        fecha = timezone.now().date()
    
    pedidos_asignados = Pedido.objects.filter(
        idRepartidor=repartidor,
        estado_pedido__in=['En Camino', 'Confirmado'],
        fechaCreacion__date=fecha
    ).count()
    
    capacidad_restante = PEDIDOS_POR_REPARTIDOR - pedidos_asignados
    return max(0, capacidad_restante)


def asignar_pedidos_automaticamente(fecha=None):
    """
    Asigna automáticamente los pedidos a los repartidores disponibles.
    Retorna un diccionario con información sobre la asignación.
    """
    if fecha is None:
        fecha = timezone.now().date()
    
    resultado = {
        'pedidos_asignados': 0,
        'pedidos_agendados': 0,
        'repartidores_sin_capacidad': False,
        'mensaje': ''
    }
    
    pedidos_sin_asignar = obtener_pedidos_sin_asignar(fecha)
    repartidores = obtener_repartidores_disponibles()
    
    if not repartidores.exists():
        resultado['repartidores_sin_capacidad'] = True
        resultado['mensaje'] = f"No hay repartidores disponibles para {len(pedidos_sin_asignar)} pedidos"
        return resultado
    
    # Asignar pedidos a repartidores
    for pedido in pedidos_sin_asignar:
        # Buscar un repartidor con capacidad
        repartidor_asignado = None
        
        for repartidor in repartidores:
            capacidad = calcular_capacidad_repartidor(repartidor, fecha)
            if capacidad > 0:
                repartidor_asignado = repartidor
                break
        
        if repartidor_asignado:
            # Asignar el pedido
            pedido.idRepartidor = repartidor_asignado
            pedido.estado_pedido = 'En Camino'
            pedido.save()
            resultado['pedidos_asignados'] += 1
        else:
            # Agendar para el día siguiente
            fecha_siguiente = fecha + timedelta(days=1)
            # Aquí podrías guardar una nota o cambiar el estado
            resultado['pedidos_agendados'] += 1
            resultado['repartidores_sin_capacidad'] = True
    
    if resultado['repartidores_sin_capacidad']:
        resultado['mensaje'] = f"Se asignaron {resultado['pedidos_asignados']} pedidos. {resultado['pedidos_agendados']} pedidos se agendarán para mañana (sin capacidad de repartidores)"
    else:
        resultado['mensaje'] = f"Se asignaron exitosamente {resultado['pedidos_asignados']} pedidos"
    
    return resultado


def generar_pdf_pedidos_repartidor(repartidor, fecha=None):
    """
    Genera un PDF con todos los pedidos asignados a un repartidor para un día específico
    """
    if fecha is None:
        fecha = timezone.now().date()
    
    pedidos = Pedido.objects.filter(
        idRepartidor=repartidor,
        estado_pedido__in=['En Camino', 'Confirmado'],
        fechaCreacion__date=fecha
    ).select_related('idCliente').prefetch_related('detallepedido_set__idProducto')
    
    # Calcular horarios de entrega
    pedidos_con_horario = []
    hora_inicio = HORARIO_INICIO
    
    for idx, pedido in enumerate(pedidos):
        hora_fin = hora_inicio + (TIEMPO_ENTREGA_MINUTOS // 60)
        pedidos_con_horario.append({
            'pedido': pedido,
            'hora_inicio': f"{hora_inicio:02d}:00",
            'hora_fin': f"{hora_fin:02d}:00",
            'numero_secuencia': idx + 1
        })
        hora_inicio = hora_fin
    
    context = {
        'repartidor': repartidor,
        'pedidos': pedidos_con_horario,
        'fecha': fecha,
        'total_pedidos': len(pedidos_con_horario),
        'horario_inicio': f"{HORARIO_INICIO:02d}:00",
        'horario_fin': f"{HORARIO_FIN:02d}:00"
    }
    
    template_path = 'asignacion_pedidos_repartidor_pdf.html'
    from django.template.loader import get_template
    template = get_template(template_path)
    html = template.render(context)
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    
    return None


def enviar_correo_repartidor_detallado(repartidor, fecha=None):
    """
    Envía un correo detallado al repartidor con información sobre sus pedidos y cómo organizar la ruta
    """
    if fecha is None:
        fecha = timezone.now().date()
    
    print(f"[DEBUG] Iniciando envío de correo para repartidor: {repartidor.nombreRepartidor}")
    print(f"[DEBUG] Email del repartidor: {repartidor.email}")
    
    if not repartidor.email:
        logger.warning(f"El repartidor {repartidor.nombreRepartidor} no tiene correo registrado")
        print(f"[DEBUG] ERROR: Repartidor sin email")
        return False
    
    try:
        # Obtener TODOS los pedidos pendientes del repartidor (sin filtro de fecha)
        # Mostrar todos los pedidos que están en estado 'En Camino' o 'Confirmado'
        
        todos_pedidos = Pedido.objects.filter(
            idRepartidor=repartidor,
            estado_pedido__in=['En Camino', 'Confirmado']
        ).select_related('idCliente').prefetch_related('detallepedido_set__idProducto').order_by('fechaCreacion')
        
        if not todos_pedidos.exists():
            logger.info(f"No hay pedidos para {repartidor.nombreRepartidor}")
            print(f"[DEBUG] No hay pedidos para procesar")
            return False
        
        # Preparar información de pedidos
        pedidos_con_info = []
        
        for idx, pedido in enumerate(todos_pedidos, 1):
            # Calcular fecha de vencimiento si no existe
            if not pedido.fecha_vencimiento:
                ciudad = 'Soacha' if 'soacha' in pedido.idCliente.direccion.lower() else 'Bogotá'
                fecha_vencimiento = calcular_fecha_vencimiento(pedido.fechaCreacion.date(), ciudad)
                pedido.fecha_vencimiento = fecha_vencimiento
                pedido.save()
            else:
                fecha_vencimiento = pedido.fecha_vencimiento
            
            # Calcular días restantes
            dias_restantes = (fecha_vencimiento - timezone.now().date()).days
            alerta = 'VENCE HOY' if dias_restantes == 0 else f'Vence en {dias_restantes} días' if dias_restantes > 0 else 'VENCIDO'
            
            # Extraer ciudad/municipio de la dirección
            direccion_completa = pedido.idCliente.direccion or ''
            ciudad_municipio = 'Soacha' if 'soacha' in direccion_completa.lower() else 'Bogotá'
            
            # Extraer comuna si está disponible
            partes_direccion = direccion_completa.split(',')
            comuna = partes_direccion[-1].strip() if len(partes_direccion) > 1 else ''
            
            # Estado de pago para cobro
            cobra_envio = 'SÍ' if pedido.estado_pago == 'Pago Parcial' else 'NO'
            
            pedidos_con_info.append({
                'pedido': pedido,
                'numero_secuencia': idx,
                'numero_pedido': pedido.idPedido,
                'cliente_nombre': pedido.idCliente.nombre,
                'cliente_telefono': pedido.idCliente.telefono,
                'cliente_direccion': direccion_completa,
                'ciudad_municipio': ciudad_municipio,
                'comuna': comuna,
                'total_pedido': pedido.total,
                'estado_pago': pedido.estado_pago,
                'estado_pago_texto': 'Pagado' if pedido.estado_pago == 'Pago Completo' else 'Pago Parcial',
                'cobra_envio': cobra_envio,
                'productos_count': pedido.detallepedido_set.count(),
                'fecha_pedido': pedido.fechaCreacion.date().strftime('%d/%m/%Y'),
                'fecha_vencimiento': fecha_vencimiento.strftime('%d/%m/%Y'),
                'dias_restantes': dias_restantes,
                'alerta': alerta
            })
        
        # Preparar el correo HTML
        mes_actual = fecha.strftime('%B de %Y')
        subject = f"Plan Mensual de Entregas - {repartidor.nombreRepartidor} - {mes_actual}"
        
        # Generar tabla de pedidos
        tabla_pedidos = ""
        for item in pedidos_con_info:
            estado_pago_color = "#6b7280" if item['estado_pago'] == 'Pago Completo' else "#9a3412"
            
            # Color de alerta según días restantes
            alerta_color = "#dc2626" if item['dias_restantes'] <= 0 else "#f97316" if item['dias_restantes'] == 1 else "#6b7280"
            
            tabla_pedidos += f"""
            <div style="background-color: {'#fef2f2' if item['dias_restantes'] <= 0 else '#f8fafc'}; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 15px; border-left: 4px solid {alerta_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">
                    <h4 style="margin: 0; color: #7c3aed; font-size: 14px;">PEDIDO #{item['numero_pedido']} - {item['cliente_nombre']}</h4>
                    <span style="background-color: {alerta_color}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: bold;">{item['alerta']}</span>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 12px;">
                    <div>
                        <p style="margin: 3px 0; color: #374151;"><strong>Teléfono:</strong> {item['cliente_telefono']}</p>
                        <p style="margin: 3px 0; color: #374151;"><strong>Dirección:</strong> {item['cliente_direccion']}</p>
                        <p style="margin: 3px 0; color: #374151;"><strong>Ciudad:</strong> {item['ciudad_municipio']}</p>
                    </div>
                    <div>
                        <p style="margin: 3px 0; color: {estado_pago_color}; font-weight: bold;"><strong>Estado Pago:</strong> {item['estado_pago_texto']}</p>
                        <p style="margin: 3px 0; color: {'#dc2626' if item['cobra_envio'] == 'SÍ' else '#6b7280'}; font-weight: bold;"><strong>¿Cobrar Envío?:</strong> {item['cobra_envio']}</p>
                        <p style="margin: 3px 0; color: #374151; font-weight: bold;"><strong>Total:</strong> ${item['total_pedido']}</p>
                        <p style="margin: 3px 0; color: {alerta_color}; font-weight: bold;"><strong>Vencimiento:</strong> {item['fecha_vencimiento']}</p>
                    </div>
                </div>
            </div>
            """
        
        html_message = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #faf8ff; margin: 0; padding: 0; }}
                .container {{ max-width: 900px; margin: 20px auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #e8d5ff 0%, #f0e6ff 100%); color: #6b46c1; padding: 30px; text-align: center; border-bottom: 3px solid #c4b5fd; }}
                .logo {{ width: 80px; height: 80px; margin: 0 auto 15px; background: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 10px rgba(107, 70, 193, 0.2); }}
                .logo-text {{ font-size: 24px; font-weight: bold; color: #6b46c1; }}
                .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; color: #6b46c1; }}
                .header p {{ margin: 10px 0 0 0; font-size: 14px; opacity: 0.8; color: #7c3aed; }}
                .content {{ padding: 30px; }}
                .info-section {{ background-color: #f3f0ff; border-left: 5px solid #c4b5fd; padding: 20px; margin-bottom: 25px; border-radius: 6px; }}
                .info-section h3 {{ color: #7c3aed; margin-top: 0; font-size: 16px; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px; }}
                .info-item {{ font-size: 14px; color: #6b7280; }}
                .info-item strong {{ color: #374151; }}
                .pedidos-lista {{ margin: 20px 0; }}
                .pedido-card {{ background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 15px; }}
                .pedido-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
                .pedido-info {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 12px; }}
                .recomendaciones {{ background-color: #fef7ed; border-left: 5px solid #f97316; padding: 20px; margin-top: 25px; border-radius: 6px; }}
                .recomendaciones h3 {{ color: #ea580c; margin-top: 0; font-size: 16px; }}
                .recomendaciones ul {{ margin: 10px 0; padding-left: 20px; }}
                .recomendaciones li {{ margin: 8px 0; color: #9a3412; font-size: 14px; }}
                .footer {{ background-color: #faf8ff; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb; color: #9ca3af; font-size: 12px; }}
                .resumen {{ background-color: #f3f0ff; border-left: 5px solid #c4b5fd; padding: 20px; margin-bottom: 25px; border-radius: 6px; }}
                .resumen h3 {{ color: #7c3aed; margin-top: 0; font-size: 16px; }}
                .resumen-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 10px; }}
                .resumen-item {{ text-align: center; }}
                .resumen-numero {{ font-size: 24px; font-weight: bold; color: #7c3aed; }}
                .resumen-label {{ font-size: 12px; color: #6b7280; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Glam Store</h1>
                    <p>Ruta de Entregas - {fecha.strftime('%A, %d de %B de %Y')}</p>
                </div>
                
                <div class="content">
                    <p>Hola <strong>{repartidor.nombreRepartidor}</strong>,</p>
                    
                    <p>Te enviamos el plan mensual de entregas para {mes_actual}. A continuación encontrarás todos los pedidos que debes entregar con la información completa de ubicación y estado de pago. Por favor, revisa cuidadosamente cada detalle para optimizar tu ruta.</p>
                    
                    <div class="resumen">
                        <h3>Resumen de tu Jornada</h3>
                        <div class="resumen-grid">
                            <div class="resumen-item">
                                <div class="resumen-numero">{len(pedidos_con_info)}</div>
                                <div class="resumen-label">Pedidos a Entregar</div>
                            </div>
                            <div class="resumen-item">
                                <div class="resumen-numero">6:00 AM - 3:00 PM</div>
                                <div class="resumen-label">Horario de Trabajo</div>
                            </div>
                            <div class="resumen-item">
                                <div class="resumen-numero">12:00 - 12:30</div>
                                <div class="resumen-label">Almuerzo</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3>Información de tu Jornada</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <strong>Horario:</strong> 6:00 AM - 3:00 PM
                            </div>
                            <div class="info-item">
                                <strong>Almuerzo:</strong> 12:00 - 12:30
                            </div>
                            <div class="info-item">
                                <strong>Total de pedidos:</strong> {len(pedidos_con_info)}
                            </div>
                        </div>
                    </div>
                    
                    <h3 style="color: #333; margin-top: 25px; margin-bottom: 15px;">Plan Mensual de Entregas</h3>
                    <p style="color: #666; font-size: 14px; margin-bottom: 15px;">
                        <strong>Repartidor:</strong> {repartidor.nombreRepartidor} | <strong>Total de pedidos:</strong> {len(pedidos_con_info)} | <strong>Mes:</strong> {mes_actual}
                    </p>
                    <div class="pedidos-lista">
                        {tabla_pedidos}
                    </div>
                    
                    <div class="recomendaciones">
                        <h3>Recomendaciones para Optimizar tu Ruta</h3>
                        <ul>
                            <li><strong>Confirmación Previa:</strong> Llama al cliente <strong>15 minutos antes de llegar</strong> para confirmar su disponibilidad y asegurar que esté en casa.</li>
                            <li><strong>Confirmar Recepción:</strong> Dile al cliente que registre en la plataforma que <strong>recibió su pedido</strong> correctamente.</li>
                            <li><strong>Evidencia Fotográfica:</strong> Dile al cliente que se tome una foto con el pedido para evidenciar que sí fue recibido.</li>
                            <li><strong>Calificación del Servicio:</strong> Pide al cliente que <strong>califica tu servicio</strong> en la plataforma. Tu opinión es importante para mejorar continuamente.</li>
                        </ul>
                    </div>
                    
                    <p style="margin-top: 25px; color: #666; font-size: 14px;">
                        Si tienes preguntas o necesitas ayuda, contacta al equipo de soporte en <strong>glamstore0303777@gmail.com</strong>
                    </p>
                </div>
                
                <div class="footer">
                    <p><strong>Glam Store - Sistema de Entregas</strong></p>
                    <p>Este es un correo automático. Por favor, no respondas a este mensaje.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Crear y enviar el correo
        email = EmailMultiAlternatives(
            subject=subject,
            body=strip_tags(html_message),
            from_email='glamstore0303777@gmail.com',
            to=[repartidor.email]
        )
        
        email.attach_alternative(html_message, "text/html")
        
        # Generar y adjuntar PDF
        print(f"[DEBUG] Generando PDF para repartidor {repartidor.idRepartidor}")
        try:
            pdf_content = generar_pdf_pedidos_repartidor(repartidor, fecha)
            if pdf_content:
                print(f"[DEBUG] PDF generado exitosamente, tamaño: {len(pdf_content)} bytes")
                email.attach(
                    f'ruta_entregas_{repartidor.idRepartidor}_{fecha.strftime("%Y%m%d")}.pdf',
                    pdf_content,
                    'application/pdf'
                )
            else:
                print(f"[DEBUG] No se pudo generar el PDF")
        except Exception as pdf_error:
            print(f"[DEBUG] Error al generar PDF: {str(pdf_error)}")
            # Continuar sin PDF si hay error
        
        # Enviar
        print(f"[DEBUG] Enviando correo a {repartidor.email}")
        print(f"[DEBUG] Asunto: {subject}")
        print(f"[DEBUG] Destinatarios: {email.to}")
        print(f"[DEBUG] Configuración EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'No configurado')}")
        print(f"[DEBUG] Configuración EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'No configurado')}")
        
        resultado = email.send()
        print(f"[DEBUG] Resultado del envío: {resultado}")
        
        if resultado > 0:
            logger.info(f"Correo de ruta enviado exitosamente a {repartidor.email}")
            return True
        else:
            print(f"[DEBUG] El envío falló - resultado: {resultado}")
            return False
        
    except Exception as e:
        print(f"[DEBUG] ERROR al enviar correo: {str(e)}")
        import traceback
        traceback.print_exc()
        logger.error(f"Error al enviar correo al repartidor: {str(e)}")
        return False


def enviar_pdf_repartidor(repartidor, email_repartidor, fecha=None):
    """
    Genera y envía por correo el PDF con los pedidos del repartidor
    (Función heredada - ahora usa enviar_correo_repartidor_detallado)
    """
    return enviar_correo_repartidor_detallado(repartidor, fecha)


def verificar_capacidad_repartidores(fecha=None):
    """
    Verifica si hay suficientes repartidores para los pedidos del día.
    Retorna True si hay capacidad, False si no.
    """
    if fecha is None:
        fecha = timezone.now().date()
    
    pedidos_sin_asignar = obtener_pedidos_sin_asignar(fecha).count()
    repartidores = obtener_repartidores_disponibles()
    
    if not repartidores.exists():
        return pedidos_sin_asignar == 0
    
    capacidad_total = sum(
        calcular_capacidad_repartidor(r, fecha) for r in repartidores
    )
    
    return capacidad_total >= pedidos_sin_asignar

def obtener_ruta_logo():
    """
    Obtiene la ruta del logo para incluir en el PDF
    """
    try:
        # Buscar en core/static/img/
        logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'img', 'logoglam.png')
        if os.path.exists(logo_path):
            print(f"[DEBUG] Logo encontrado en: {logo_path}")
            # Convertir a formato file:// para xhtml2pdf en Windows
            logo_path = logo_path.replace('\\', '/')
            return f"file:///{logo_path}"
        else:
            print(f"[DEBUG] Logo NO encontrado en: {logo_path}")
            # Intentar ruta alternativa
            logo_path_alt = os.path.join(settings.BASE_DIR, 'static', 'img', 'logoglam.png')
            if os.path.exists(logo_path_alt):
                print(f"[DEBUG] Logo encontrado en ruta alternativa: {logo_path_alt}")
                logo_path_alt = logo_path_alt.replace('\\', '/')
                return f"file:///{logo_path_alt}"
    except Exception as e:
        print(f"[DEBUG] Error al obtener ruta del logo: {str(e)}")
    return None


def generar_pdf_pedidos_repartidor(repartidor, fecha=None):
    """
    Genera un PDF con TODOS los pedidos pendientes del repartidor
    """
    if fecha is None:
        fecha = timezone.now().date()
    
    try:
        # Obtener TODOS los pedidos pendientes del repartidor (sin filtro de fecha)
        todos_pedidos = Pedido.objects.filter(
            idRepartidor=repartidor,
            estado_pedido__in=['En Camino', 'Confirmado']
        ).select_related('idCliente').prefetch_related('detallepedido_set__idProducto').order_by('fechaCreacion')
        
        if not todos_pedidos.exists():
            return None
        
        # Preparar información de pedidos
        pedidos_con_info = []
        
        for idx, pedido in enumerate(todos_pedidos, 1):
            estado_pago_texto = "Pagado" if pedido.estado_pago == 'Pago Completo' else "Pago Parcial"
            
            # Calcular fecha de vencimiento si no existe
            if not pedido.fecha_vencimiento:
                ciudad = 'Soacha' if 'soacha' in pedido.idCliente.direccion.lower() else 'Bogotá'
                fecha_vencimiento = calcular_fecha_vencimiento(pedido.fechaCreacion.date(), ciudad)
                pedido.fecha_vencimiento = fecha_vencimiento
                pedido.save()
            else:
                fecha_vencimiento = pedido.fecha_vencimiento
            
            # Calcular días restantes
            dias_restantes = (fecha_vencimiento - timezone.now().date()).days
            alerta = 'VENCE HOY' if dias_restantes == 0 else f'Vence en {dias_restantes} días' if dias_restantes > 0 else 'VENCIDO'
            
            # Extraer ciudad/municipio y comuna
            direccion_completa = pedido.idCliente.direccion or ''
            ciudad_municipio = 'Soacha' if 'soacha' in direccion_completa.lower() else 'Bogotá'
            partes_direccion = direccion_completa.split(',')
            comuna = partes_direccion[-1].strip() if len(partes_direccion) > 1 else ''
            
            # Estado de pago para cobro
            cobra_envio = 'SÍ' if pedido.estado_pago == 'Pago Parcial' else 'NO'
            
            pedidos_con_info.append({
                'numero_pedido': pedido.idPedido,
                'cliente': pedido.idCliente.nombre,
                'telefono': pedido.idCliente.telefono,
                'direccion': direccion_completa,
                'ciudad_municipio': ciudad_municipio,
                'comuna': comuna,
                'total': pedido.total,
                'estado_pago': estado_pago_texto,
                'cobra_envio': cobra_envio,
                'fecha_pedido': pedido.fechaCreacion.date().strftime('%d/%m/%Y'),
                'fecha_vencimiento': fecha_vencimiento.strftime('%d/%m/%Y'),
                'alerta': alerta
            })
        
        # Crear HTML para el PDF - formato de lista
        lista_pedidos = ""
        for idx, item in enumerate(pedidos_con_info, 1):
            color_alerta = "#dc2626" if 'VENCE' in item['alerta'] or 'VENCIDO' in item['alerta'] else "#6b7280"
            color_cobro = "#dc2626" if item['cobra_envio'] == 'SÍ' else "#6b7280"
            
            lista_pedidos += f"""
            <div class="pedido-item" style="background-color: {'#fef2f2' if 'VENCE' in item['alerta'] or 'VENCIDO' in item['alerta'] else '#f8fafc'}; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 15px; page-break-inside: avoid;">
                <div class="pedido-header" style="border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 10px;">
                    <h4 style="margin: 0; color: #7c3aed; font-size: 14px;">PEDIDO #{item['numero_pedido']} - {item['cliente']}</h4>
                    <p style="margin: 2px 0; font-size: 11px; color: {color_alerta}; font-weight: bold;">{item['alerta']}</p>
                </div>
                
                <div class="pedido-info" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 11px;">
                    <div>
                        <p style="margin: 3px 0;"><strong>Teléfono:</strong> {item['telefono']}</p>
                        <p style="margin: 3px 0;"><strong>Dirección:</strong> {item['direccion']}</p>
                        <p style="margin: 3px 0;"><strong>Ciudad:</strong> {item['ciudad_municipio']}</p>
                        <p style="margin: 3px 0;"><strong>Comuna:</strong> {item['comuna']}</p>
                    </div>
                    <div>
                        <p style="margin: 3px 0;"><strong>Estado Pago:</strong> {item['estado_pago']}</p>
                        <p style="margin: 3px 0; color: {color_cobro}; font-weight: bold;"><strong>¿Cobrar Envío?:</strong> {item['cobra_envio']}</p>
                        <p style="margin: 3px 0;"><strong>Total:</strong> ${item['total']}</p>
                        <p style="margin: 3px 0;"><strong>Vencimiento:</strong> {item['fecha_vencimiento']}</p>
                    </div>
                </div>
            </div>
            """
        
        # Obtener ruta del logo
        logo_path = obtener_ruta_logo()
        if logo_path:
            logo_html = f'<img src="{logo_path}" style="width: 80px; height: 80px; object-fit: contain;" />'
        else:
            logo_html = ''
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 15px; font-size: 12px; line-height: 1.4; background-color: #faf8ff; }}
                .header {{ display: flex; align-items: center; gap: 20px; padding: 20px; background: linear-gradient(135deg, #e8d5ff 0%, #f0e6ff 100%); border-radius: 10px; margin-bottom: 20px; }}
                .logo {{ width: 80px; height: 80px; background: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(124, 58, 237, 0.2); flex-shrink: 0; }}
                .logo-text {{ font-size: 28px; font-weight: bold; color: #7c3aed; }}
                .header h1 {{ margin: 0; font-size: 32px; color: #7c3aed; font-weight: 700; letter-spacing: 1px; }}
                .header p {{ margin: 5px 0 0 0; font-size: 12px; color: #6b7280; }}
                .info-section {{ background-color: #f3f0ff; padding: 10px; margin-bottom: 15px; border-left: 3px solid #c4b5fd; border-radius: 5px; }}
                .info-section h3 {{ margin: 0 0 8px 0; color: #7c3aed; font-size: 13px; }}
                .info-section p {{ margin: 3px 0; font-size: 11px; color: #6b7280; }}
                .pedidos-container {{ margin: 15px 0; }}
                .pedidos-title {{ color: #374151; font-size: 14px; font-weight: bold; margin-bottom: 15px; border-bottom: 2px solid #c4b5fd; padding-bottom: 5px; }}
                .pedido-item {{ background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 15px; page-break-inside: avoid; }}
                .pedido-header {{ border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 10px; }}
                .pedido-header h4 {{ margin: 0; color: #7c3aed; font-size: 14px; }}
                .pedido-info {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 11px; }}
                .footer {{ margin-top: 20px; text-align: center; color: #9ca3af; font-size: 10px; }}
            </style>
        </head>
        <body>
            <div class="header" style="display: flex; align-items: center; gap: 20px; padding: 20px; background: linear-gradient(135deg, #e8d5ff 0%, #f0e6ff 100%); border-radius: 10px; margin-bottom: 20px;">
                <div style="flex-shrink: 0;">
                    <div class="logo" style="width: 80px; height: 80px; background: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(124, 58, 237, 0.2);">
                        {logo_html}
                    </div>
                </div>
                <div style="flex-grow: 1;">
                    <h1 style="margin: 0; font-size: 32px; color: #7c3aed; font-weight: 700; letter-spacing: 1px;">Glam Store</h1>
                    <p style="margin: 5px 0 0 0; font-size: 14px; color: #6b46c1; font-weight: 500;">Plan Mensual de Entregas</p>
                    <p style="margin: 8px 0 0 0; font-size: 12px; color: #6b7280;"><strong>Repartidor:</strong> {repartidor.nombreRepartidor} | <strong>Mes:</strong> {fecha.strftime('%B de %Y')}</p>
                </div>
            </div>
            
            <div class="info-section">
                <h3>Información de la Jornada</h3>
                <p><strong>Horario:</strong> 6:00 AM - 3:00 PM (Almuerzo: 12:00 - 12:30)</p>
                <p><strong>Total de pedidos:</strong> {len(pedidos_con_info)}</p>
            </div>
            
            <div class="pedidos-container">
                <h3 class="pedidos-title">Lista de Pedidos a Entregar</h3>
                {lista_pedidos}
            </div>
            
            <div class="info-section" style="background-color: #fef7ed; border-left: 3px solid #f97316; margin-top: 20px;">
                <h3 style="color: #ea580c;">Recomendaciones para Optimizar tu Ruta</h3>
                <p style="color: #9a3412;"><strong>Confirmación Previa:</strong> Llama al cliente <strong>15 minutos antes de llegar</strong> para confirmar su disponibilidad.</p>
                <p style="color: #9a3412;"><strong>Confirmar Recepción:</strong> Dile al cliente que registre en la plataforma que <strong>recibió su pedido</strong> correctamente.</p>
                <p style="color: #9a3412;"><strong>Evidencia Fotográfica:</strong> Dile al cliente que se tome una foto con el pedido para evidenciar que sí fue recibido.</p>
                <p style="color: #9a3412;"><strong>Calificación del Servicio:</strong> Pide al cliente que <strong>califica tu servicio</strong> en la plataforma.</p>
            </div>
            
            <div class="footer">
                <p><strong>Glam Store - Sistema de Entregas</strong></p>
                <p>Documento generado automáticamente</p>
            </div>
        </body>
        </html>
        """
        
        # Generar PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)
        
        if not pdf.err:
            return result.getvalue()
        else:
            print(f"[DEBUG] Error al generar PDF: {pdf.err}")
            return None
            
    except Exception as e:
        print(f"[DEBUG] Error en generar_pdf_pedidos_repartidor: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
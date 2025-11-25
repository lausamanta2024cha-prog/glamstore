#!/usr/bin/env python
"""
Script para probar el envío de correos a repartidores
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.utils import timezone
from core.models.repartidores import Repartidor
from core.models.pedidos import Pedido
from core.Gestion_admin.services_repartidores import enviar_correo_repartidor_detallado
from django.conf import settings

def test_configuracion_email():
    """Prueba la configuración de email"""
    print("=== VERIFICANDO CONFIGURACIÓN DE EMAIL ===")
    print(f"EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'No configurado')}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'No configurado')}")
    print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'No configurado')}")
    print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'No configurado')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'No configurado')}")
    print(f"EMAIL_HOST_PASSWORD: {'***configurado***' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else 'No configurado'}")
    print()

def test_envio_correo_simple():
    """Prueba el envío de un correo simple"""
    print("=== PROBANDO ENVÍO DE CORREO SIMPLE ===")
    try:
        from django.core.mail import send_mail
        
        resultado = send_mail(
            'Prueba de correo',
            'Este es un correo de prueba desde Django.',
            settings.EMAIL_HOST_USER,
            ['glamstore0303777@gmail.com'],  # Enviar a la misma cuenta
            fail_silently=False,
        )
        print(f"Resultado del envío simple: {resultado}")
        return resultado > 0
    except Exception as e:
        print(f"Error en envío simple: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_repartidores_con_email():
    """Verifica qué repartidores tienen email configurado"""
    print("=== VERIFICANDO REPARTIDORES CON EMAIL ===")
    repartidores = Repartidor.objects.all()
    
    for repartidor in repartidores:
        email_status = "✓" if repartidor.email else "✗"
        print(f"{email_status} {repartidor.nombreRepartidor} - Email: {repartidor.email or 'No configurado'}")
    
    repartidores_con_email = repartidores.filter(email__isnull=False).exclude(email='')
    print(f"\nTotal repartidores: {repartidores.count()}")
    print(f"Con email: {repartidores_con_email.count()}")
    print()
    
    return repartidores_con_email

def test_pedidos_repartidores():
    """Verifica qué repartidores tienen pedidos asignados hoy"""
    print("=== VERIFICANDO PEDIDOS DE REPARTIDORES HOY ===")
    fecha_hoy = timezone.now().date()
    
    repartidores_con_email = Repartidor.objects.filter(email__isnull=False).exclude(email='')
    
    for repartidor in repartidores_con_email:
        pedidos = Pedido.objects.filter(
            idRepartidor=repartidor,
            estado_pedido__in=['En Camino', 'Confirmado'],
            fechaCreacion__date=fecha_hoy
        )
        
        pedidos_count = pedidos.count()
        status = "✓" if pedidos_count > 0 else "✗"
        print(f"{status} {repartidor.nombreRepartidor} - Pedidos hoy: {pedidos_count}")
    
    print()

def test_envio_correo_repartidor():
    """Prueba el envío de correo a un repartidor específico"""
    print("=== PROBANDO ENVÍO DE CORREO A REPARTIDOR ===")
    
    # Buscar un repartidor con email
    repartidor = Repartidor.objects.filter(email__isnull=False).exclude(email='').first()
    
    if not repartidor:
        print("No hay repartidores con email configurado")
        return False
    
    print(f"Probando envío a: {repartidor.nombreRepartidor} ({repartidor.email})")
    
    try:
        resultado = enviar_correo_repartidor_detallado(repartidor)
        print(f"Resultado del envío: {resultado}")
        return resultado
    except Exception as e:
        print(f"Error en envío a repartidor: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("INICIANDO PRUEBAS DE ENVÍO DE CORREOS")
    print("=" * 50)
    
    # 1. Verificar configuración
    test_configuracion_email()
    
    # 2. Probar envío simple
    if not test_envio_correo_simple():
        print("❌ El envío simple falló. Revisa la configuración de email.")
        return
    else:
        print("✅ El envío simple funcionó correctamente.")
        print()
    
    # 3. Verificar repartidores
    repartidores_con_email = test_repartidores_con_email()
    
    # 4. Verificar pedidos
    test_pedidos_repartidores()
    
    # 5. Probar envío a repartidor
    if test_envio_correo_repartidor():
        print("✅ El envío a repartidor funcionó correctamente.")
    else:
        print("❌ El envío a repartidor falló.")
    
    print("\nPRUEBAS COMPLETADAS")

if __name__ == "__main__":
    main()
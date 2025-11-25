#!/usr/bin/env python
"""
Script para simular el envío desde la interfaz web
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from core.Gestion_admin.views import enviar_correos_repartidores_seleccionados_view
from core.models.repartidores import Repartidor

def simular_envio_web():
    """Simula el envío desde la interfaz web"""
    print("=== SIMULANDO ENVÍO DESDE INTERFAZ WEB ===")
    
    # Obtener repartidores con email
    repartidores_con_email = Repartidor.objects.filter(email__isnull=False).exclude(email='')
    
    if not repartidores_con_email.exists():
        print("❌ No hay repartidores con email")
        return
    
    # Seleccionar el primer repartidor
    repartidor_seleccionado = repartidores_con_email.first()
    print(f"Repartidor seleccionado: {repartidor_seleccionado.nombreRepartidor} (ID: {repartidor_seleccionado.idRepartidor})")
    
    # Crear request factory
    factory = RequestFactory()
    
    # Simular datos POST como los enviaría el formulario
    post_data = {
        'repartidor_ids': [str(repartidor_seleccionado.idRepartidor)],
        'csrfmiddlewaretoken': 'test-token'
    }
    
    print(f"Datos POST simulados: {post_data}")
    
    # Crear request POST
    request = factory.post('/repartidores/enviar_correos_seleccionados/', post_data)
    
    print("🔄 Ejecutando vista...")
    
    try:
        # Ejecutar la vista directamente
        from core.Gestion_admin.views import enviar_correos_repartidores_seleccionados_view
        
        # Simular el procesamiento manual
        print("📋 Procesando repartidor seleccionado...")
        
        from django.utils import timezone
        from core.models.pedidos import Pedido
        from core.Gestion_admin.services_repartidores import enviar_correo_repartidor_detallado
        
        fecha = timezone.now().date()
        
        # Verificar que tenga email
        if not repartidor_seleccionado.email:
            print("❌ El repartidor no tiene email")
            return
        
        # Verificar que tenga pedidos
        pedidos = Pedido.objects.filter(
            idRepartidor=repartidor_seleccionado,
            estado_pedido__in=['En Camino', 'Confirmado'],
            fechaCreacion__date=fecha
        ).count()
        
        print(f"📦 Pedidos encontrados: {pedidos}")
        
        if pedidos == 0:
            print("❌ No tiene pedidos para hoy")
            return
        
        # Intentar enviar correo
        print("📧 Enviando correo...")
        resultado = enviar_correo_repartidor_detallado(repartidor_seleccionado, fecha)
        
        if resultado:
            print("✅ Correo enviado exitosamente")
        else:
            print("❌ Error al enviar correo")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal"""
    print("INICIANDO SIMULACIÓN DE INTERFAZ WEB")
    print("=" * 50)
    
    simular_envio_web()
    
    print("\nSIMULACIÓN COMPLETADA")

if __name__ == "__main__":
    main()